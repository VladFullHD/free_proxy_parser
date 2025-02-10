import requests
from bs4 import BeautifulSoup
import time
import csv
import os
import re
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium_stealth import stealth
from urllib3.util import url


# Объединение наименования папки и наименования файла, тем самым создается путь к файлу
def html_file_path(html_folder, html_filename):
    return os.path.join(html_folder, html_filename)

# Проверка на наличие папки для хранения HTML-страниц
def html_folder_exists(html_folder):
    if os.path.isdir(html_folder):
        print(f'Папка "{html_folder}" найдена!')
        return True
    else:
        print(f'Папка "{html_folder}" не найдена!')

# Проверка на наличие HTML-страницы
def html_file_exists(html_filename, html_path):
    if os.path.exists(html_path):
        print(f'Файл "{html_filename}" найден!')
        return True
    else:
        print(f'Файл "{html_filename}" не найден!')
        return False

# Создание папки с определенным названием для хранения HTML-страниц
def create_html_folder(html_folder):
    try:
        os.makedirs(html_folder, exist_ok=True)
        print(f'Папка под названием "{html_folder}" успешно создана!')
        return True
    except Exception as e:
        print(f'Произошла ошибка при создании папки "{html_folder}": {e}')
        return False

# Сохранение HTML-страницы под определенным названием по необходимому пути
def save_html_file(html, html_path):
    try:
        with open(html_path, 'w', encoding='utf-8') as f:
            f.write(html)
        print(f'HTML-код страницы успешно сохранен в: {html_path}')
    except Exception as e:
        print(f'Ошибка записи в файл: {e}')
        return []

# Чтение HTML-страницы и запись в переменную "html"
def open_html_file(html_path):
    try:
        with open(html_path, 'r', encoding='utf-8') as f:
            html = f.read()
        return html
    except FileNotFoundError:
        print(f"Ошибка: Файл {html_path} не найден.")
        return None
    except Exception as e:
        print(f"Ошибка при открытии файла {html_path}: {e}")
        return None


def url_from_user():
    while True:
        url = input('Введите URL-адрес страницы (или нажмите Ctrl+C для выхода): ')
        if url.lower() == 'exit':
            return None
        if url:
            return url
        print('URL-адрес не может быть пустым. Пожалуйста, попробуйте еще раз.')


def url_to_domain(url):
    if not url:
        print('URL-адрес не может быть пустым!')
        return None

    match = re.search(r"//(?:www\.)?([^/]+)", url)
    if match:
        print(match)
        return match.group(1).split(".")[0]
    else:
        return url.split(".")[0]


def domain_to_filename(domain):
    if not domain:
        print('sfds')
        return 'default_filename.html'
    filename = domain.replace("://", "_").replace("/", "_").replace(".", "_") + ".html"  # Заменяем недопустимые символы
    return filename


def url_to_filename(url):
    domain = url_to_domain(url)
    print(domain_to_filename(domain))
    return domain_to_filename(domain)

def start_or_skip_html_code_collection(html_folder, html_filename, html_path):
    """
    Логика процесса запуска функций сбора HTML-страницы и обработки HTML-страницы.
    Проверяет, существует ли HTML-страница для последующей обработки:
    В случае True - запускает функцию обработки HTML-страницы.
    В случае False - запускает функцию сбора HTML-страницы, после чего запускается функция обработки.
    """

    if html_file_exists(html_filename, html_path):
        html_file_exists(html_filename, html_path)
        process_html_code()
    else:
        if not html_folder_exists(html_folder):
            html_file_exists(html_filename, html_path)
            create_html_folder(html_folder)
        html_file = collect_html_code()
        if html_file:
            process_html_code()
        else:
            print('Сбор HTML-кода не удался!')


def collect_html_code(url: str,
                   html_directory='html_data',
                   html_filename='proxies.html',
                   csv_directory='csv_data',
                   csv_filename='proxies.csv',
                   headers=None):
    """
    Используется для сбора необходимого HTML-кода с заданного URL-адреса.
    После получения HTML-страницы собирает все значения IP:Port и записывает их в csv-файл.

    После получения значения IP:Port при помощи функции check_proxy проверяет валидность полученных прокси.
    Проверка осуществляется при помощи get-запросов на сайт Google и только после получения положительного ответа
    на запрос IP:Port добавляется в список, после чего список сохраняется в csv-файл.
    """

    # Проверяет, существует ли файл с HTML-кодом страницы. Если да - переходит сразу к обработке HTML-кода
    if check_html_file_exists(html_directory, html_filename):
        print(f'Файл {html_path} найден. Запускаю парсинг...')
        with open(html_path, 'r', encoding='utf-8') as f:
            html = f.read()
    # Если файл с HTML-кодом страницы не найден - запускает процесс сбора кода HTML-страницы
    else:
        print(f'Файл {html_filename} не найден. Запускаю браузер и выполняю работу по сбору кода HTML-страницы...')
        os.makedirs(html_directory, exist_ok=True)
        options = webdriver.ChromeOptions()


        # Проверяет, существует ли словарь headers и добавляет заголовки в options
        if headers:
            print(f'Добавляем заголовки!')
            for key, value in headers.items():
                options.add_argument(f'--header={key}:{value}')
        else:
            print('Заголовки не были добавлены, продолжаем работу без заголовков!')

        driver = None

        try:
            '''
            Создает экземпляр веб-драйвера с заданными опциями и применяет к нему stealth
            для скрытия факта использования Selenium
            '''
            driver = webdriver.Chrome(options=options)
            stealth(driver,
                    languages=['en-US', 'en'],
                    vendor='Google Inc.',
                    platform='Win32',
                    webgl_vendor='Intel Inc.',
                    renderer='Intel Iris OpenGL Engine',
                    fix_hairline=True,
                    )

            # Открывает страницу по указанному адресу
            driver.get(url)
            time.sleep(3)

            # Клик на кнопку с выпадающим меню, в котором можно указать количество прокси, отображаемых на странице
            try:
                button = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, '//*[@id="xpp"]'))
                )
                button.click()
                time.sleep(3)
            except:
                print('Первая кнопка не найдена')
                return []

            # Клик на кнопку для отображения прокси в количестве 500 штук
            try:
                next_button = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, '//*[@id="xpp"]/option[6]'))
                )
                next_button.click()
                time.sleep(5)
            except:
                print('Вторая кнопка не найдена')
                return []

            # Получает исходный HTML-код страницы
            html = driver.page_source

            # Запись HTML-кода страницы в файл. Название файла указывает пользователь
            try:
                with open(html_path, 'w', encoding='utf-8') as f:
                    f.write(html)
                print(f'HTML-код страницы сохранён в: {html_path}')
            except Exception as e:
                print(f'Ошибка записи в файл: {e}')
                return []
        except Exception as e:
            print(f'Произошла ошибка Selenium: {e}')

        finally:
            if driver is not None:
                driver.quit()



def process_html_code():
    # Создает объект BeautifulSoup из полученной HTML-страницы для дальнейшей обработки данных
    soup = BeautifulSoup(html, 'lxml')

    # Запускает таймер для подсчета времени, затраченного на обработку и проверку прокси
    start_time = time.time()

    # Список с прокси, которые прошли проверку на валидность
    proxy_list = []

    # Счетчики для подсчета добавленных прокси
    added_count = 0 # Прошел проверку на работоспособность
    not_added_count = 0 # Не прошел проверку на работоспособность
    repeated_proxies = 0 # Дублирующийся прокси

    # Собираем информацию из атрибута класса spy1x
    tr_spy1x = soup.find_all('tr', class_='spy1x')
    for tr in tr_spy1x:
        font_spy14 = tr.find('font', class_='spy14')
        if font_spy14:
            ip = font_spy14.text.strip()
            if check_proxy(ip):
                proxy_list.append(ip)
                added_count += 1
                print(f'IP-адрес {ip} добавлен в список! Всего добавлено - < {added_count} >')
            else:
                not_added_count += 1
                print(f'Предупреждение: IP-адрес {ip} не работает и будет пропущен! Всего пропущено - < {not_added_count} >')

    # Собираем информацию из атрибута класса spy1xx
    tr_spy1xx = soup.find_all('tr', class_='spy1xx')
    for tr in tr_spy1xx:
        font_spy14 = tr.find('font', class_='spy14')
        if font_spy14:
            ip = font_spy14.text.strip()
            if check_proxy(ip):
                if ip not in proxy_list: # Проверяем, есть ли уже такой IP в списке
                    proxy_list.append(ip)
                    added_count += 1
                    print(f'IP-адрес {ip} добавлен в список! Всего добавлено - < {added_count} >')
                else:
                    repeated_proxies += 1
                    print(f'Предупреждение: IP-адрес {ip} уже существует и будет пропущен! Всего дублирующихся - < {repeated_proxies} >')
            else:
                not_added_count += 1
                print(
                    f'Предупреждение: IP-адрес {ip} не работает и будет пропущен! Всего пропущено - < {not_added_count} >')

    if proxy_list: # Если список proxies не пустой - записывает значения в csv-файл
        os.makedirs(csv_directory, exist_ok=True) # Создает директорию, в которую будет записан csv-файл
        with open(csv_path, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['IP Address'])
            for ip in proxy_list:
                writer.writerow([ip])
        print(f"IP-адреса успешно записаны в файл {csv_path}!")

        # Выводит сообщение, уведомляющее о кол-ве валидных / невалидных прокси
        print(f'Всего добавлено рабочих прокси - {added_count:5}!\n'
              f'Всего дублирующихся прокси - {repeated_proxies:5}!\n'
              f'Всего нерабочих прокси - {not_added_count:5}!\n'
              f'Итого обработано прокси - {added_count + repeated_proxies + not_added_count:5}!\n')

        # Подсчет времени, затраченного на обработку и проверку прокси
        end_time = time.time()
        elapsed_time = end_time - start_time
        minutes = int(elapsed_time // 60)
        seconds = int(elapsed_time % 60)
        print(f'Всего затрачено времени: {minutes} минут и {seconds} секунд!')

    else:
        print("Не найдено IP-адресов, соответствующих шаблону.")





def check_csv_directory_exists(csv_directory='csv_data'):
    return os.path.isdir(csv_directory)


def create_csv_directory(csv_directory='csv_data'):
    os.makedirs(csv_directory, exist_ok=True)


def save_csv_file(proxies, csv_directory='csv.data', csv_filename='proxies.csv'):
    csv_path = os.path.join(csv_directory, csv_filename)
    try:
        with open(csv_path, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['IP Address'])
            for ip in proxies:
                writer.writerow([ip])
        print(f"IP-адреса успешно записаны в файл {csv_path}!")
    except Exception as e:
        print(f'Ошибка записи в CSV-файл: {e}')
        return []


# Функция для проверки валидности прокси
def check_proxy(ip):

    try:
        proxies = {
            "http": f"socks5://{ip}",
            "https": f"socks5://{ip}",
        }
        print(f'Отправляем запрос через SOCKS5, прокси: {ip}...')
        response = requests.get("https://www.google.com", proxies=proxies, timeout=5)
        print(f'Успешно! Код ответа: {response.status_code}')
        if response.status_code == 200:
            return True
        else:
            return False
    except requests.exceptions.RequestException:
        return False


headers = {
        'accept': '*/*',
        'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36',
    }

