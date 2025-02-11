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
from fake_useragent import UserAgent



def url_from_user():
    """
    Получает URL-адрес страницы от пользователя.
    """
    while True:
        url = input('Введите URL-адрес страницы (или нажмите Ctrl+C для выхода): ')
        if url.lower() == 'exit':
            return None
        if url:
            return url



def url_to_domain(url):
    """
    Принимает в качестве аргумента URL-адрес и извлекает из него домен.

    Аргументы:
        url: URL-адрес страницы.

    Возвращает:
        Домен. Например, задан URL-адрес www.google.com. Вернет значение "google".
    """
    if not url:
        print('URL-адрес не может быть пустым!')
        return None

    match = re.search(r"//(?:www\.)?([^/]+)", url)
    if match:
        return match.group(1).split(".")[0]
    return url.split(".")[0]


def domain_to_filename(domain):
    """
    Получает в качестве аргумента наименование домена и делает из него имя файла.

    Аргументы:
        domain: Наименование домена.

    Возвращает:
        Наименование для HTML-страницы по типу: "google.com".
    """

    if not domain:
        return 'default_filename.html'
    filename = domain.replace("://", "_").replace("/", "_").replace(".", "_") + ".html"  # Заменяем недопустимые символы
    return filename


def url_to_filename(url):
    """
    Выполняет полный процесс преобразования URL-адреса в имя файла.
    Использует функции url_to_domain и domain_to_filename.

    Аргументы:
        url: URL-адрес, из которого необходимо получить имя файла для HTML-страницы.

    Возвращает:
        Имя файла для HTML-страницы в виде: "google.html"
    """
    domain = url_to_domain(url)
    if domain is None:
        return None
    html_filename = domain_to_filename(domain)
    if html_filename is None:
        print('Не удалось преобразовать URL в имя файла.')
    return html_filename


def html_file_path(html_folder, html_filename):
    """
    Объединяет наименование папки для хранения HTML-страниц и наименование файла с HTML-страницей.
    Тем самым создает путь к необходимому нам файлу.

    Аргументы:
        html_folder: Название папки для хранения HTML-страниц.
        html_filename: Название файла с HTML-страницей.

    Возвращает:
        Путь к необходимому нам файлу.
    """
    return os.path.join(html_folder, html_filename)


def html_folder_exists(html_folder):
    """
    Проверяет наличие папки для хранения HTML-страниц.

    Аргументы:
        html_folder: Название папки для хранения HTML-страниц.

    Возвращает:
        True/False - папка найдена/папка не найдена.
    """
    if os.path.isdir(html_folder):
        print(f'Папка "{html_folder}" найдена!')
        return True
    else:
        print(f'Папка "{html_folder}" не найдена!')
        return False


def html_file_exists(html_filename, html_path):
    """
    Проверяет наличие файла с HTML-страницей.

    Аргументы:
        html_filename: Наименование файла с HTML-страницей.
        html_path: Путь к файлу с HTML-страницей.

    Возвращает:
        True/False - файл найден/файл не найден.
    """
    if os.path.exists(html_path):
        print(f'Файл "{html_filename}" найден!')
        return True
    else:
        print(f'Файл "{html_filename}" не найден!')
        return False


def create_html_folder(html_folder):
    """
    Создает папку с определенным названием для хранения HTML-страниц.

    Аргументы:
        html_folder: Наименование папки для хранения HTML-страниц.

    Возвращает:
        True/False - папка успешно создана/произошла ошибка при создании папки.
    """
    try:
        os.makedirs(html_folder, exist_ok=True)
        print(f'Папка под названием "{html_folder}" успешно создана!')
        return True
    except Exception as e:
        print(f'Произошла ошибка при создании папки "{html_folder}": {e}')
        return False


def save_html_file(html, html_path):
    """
    Сохраняет HTML-страницу по заданному пути.

    Аргументы:
        html: HTML-код страницы записанный в переменную.
        html_path: Место, в которое будет сохранена HTML-страница.

    Возвращает:
        True/False - Сохранено/ошибка записи в файл.
    """
    try:
        with open(html_path, 'w', encoding='utf-8') as f:
            f.write(html)
        print(f'HTML-код страницы успешно сохранен в: {html_path}')
        return True
    except OSError as e:
        print(f'Ошибка записи в файл "{html_path}": {e}')
        return False
    except Exception as e:
        print(f'Ошибка записи в файл "{html_path}": {e}')
        return False


def open_html_file(html_path):
    """
    Читает сохраненную HTML-страницу и записывает ее в переменную.

    Аргументы:
        html_path: Путь к HTML-странице.

    Возвращает:
        Переменную "html". В случае ошибки - None - Файл не найден/Ошибка при открытии файла.
    """
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


def generate_headers(custom_headers=None):
    headers = {}

    ua = UserAgent()
    headers['User-Agent'] = ua.random

    if custom_headers:
        print(f'Добавляем заголовки, указанные пользователем!')
        headers.update(custom_headers)
    return headers


def headers_to_options(options, headers):
    for key, value in headers.items():
        options.add_argument(f'--header={key}:{value}')


def initialize_stealth_webdriver(headers=None):
    """
    Создает экземпляр веб-драйвера с заданными опциями и применяет к нему stealth для скрытия факта использования Selenium

    Аргументы:
        headers: Словарь с заголовками. По умолчанию None.
    """
    options = webdriver.ChromeOptions()
    if headers:
        headers_to_options(options, headers)
    try:
        driver = webdriver.Chrome(options=options)
        stealth(driver,
                languages=['en-US', 'en'],
                vendor='Google Inc.',
                platform='Win32',
                webgl_vendor='Intel Inc.',
                renderer='Intel Iris OpenGL Engine',
                fix_hairline=True,
                )
        return driver
    except Exception as e:
        print(f'Ошибка инициализации драйвера: {e}')
        return None


def start_or_skip_html_code_collection(html_folder, html_filename, html_path):
    """
    Логика процесса запуска функций сбора HTML-страницы и обработки HTML-страницы.
    Проверяет, существует ли HTML-страница для последующей обработки:
    В случае True - запускает функцию обработки HTML-страницы.
    В случае False - запускает функцию сбора HTML-страницы, после чего запускается функция обработки.

    Аргументы:
        html_folder: Наименование папки с HTML-страницами.
        html_filename: Наименование файла с HTML-страницей.
        html_path: Путь к файлу с HTML-страницей.
    """

    if html_file_exists(html_filename, html_path):
        html_file_exists(html_filename, html_path)
        print(f'Файл {html_filename} - не существует!')
    else:
        if not html_folder_exists(html_folder):
            html_file_exists(html_filename, html_path)
            create_html_folder(html_folder)
        html_file = collect_html_code()
        # if html_file:
        #     process_html_code()
        # else:
        #     print('Сбор HTML-кода не удался!')


def button_name_from_user():
    while True:
        button_name = input('Введите название кнопки, на которую должен нажать Selenium: ')
        if button_name.lower() == 'exit':
            return None
        if button_name:
            return button_name

def xpath_from_user():
    while True:
        xpath = input('Введите путь XPATH, который ведет к необходимой кнопке: ')
        if xpath.lower() == 'exit':
            return None
        if xpath:
            return xpath

def click_button(driver, xpath, button_name):
    try:
        button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, xpath)))
        button.click()
        time.sleep(3)
    except:
        print(f'{button_name} кнопка не найдена!')
        return False
    return True


def collect_html_code(url: str, driver, html_path, headers=None):
    """
    Используется для сбора необходимого HTML-кода с заданного URL-адреса.
    После получения HTML-страницы собирает все значения IP:Port и записывает их в csv-файл.

    После получения значения IP:Port при помощи функции check_proxy проверяет валидность полученных прокси.
    Проверка осуществляется при помощи get-запросов на сайт Google и только после получения положительного ответа
    на запрос IP:Port добавляется в список, после чего список сохраняется в csv-файл.
    """
    try:
        driver.get(url)
        time.sleep(3)

        print('Информация о первой кнопке:')
        button1_name = button_name_from_user()
        if button1_name is None:
            return None
        button1_xpath = xpath_from_user()
        if button1_xpath is None:
            return None

        if not click_button(driver, button1_xpath, button1_name):
            return None

        print("Информация о второй кнопке:")
        button2_name = button_name_from_user()
        if button2_name is None:
            return None
        button2_xpath = xpath_from_user()
        if button2_xpath is None:
            return None

        if not click_button(driver, button2_xpath, button2_name):
            return None

        html = driver.page_source

        if save_html_file(html, html_path):
            return html
        else:
            return None

    except Exception as e:
        print(f'Ошибка при сборе HTML-кода: {e}')
        return None


# def process_html_code():
#     # Создает объект BeautifulSoup из полученной HTML-страницы для дальнейшей обработки данных
#     soup = BeautifulSoup(html, 'lxml')
#
#     # Запускает таймер для подсчета времени, затраченного на обработку и проверку прокси
#     start_time = time.time()
#
#     # Список с прокси, которые прошли проверку на валидность
#     proxy_list = []
#
#     # Счетчики для подсчета добавленных прокси
#     added_count = 0 # Прошел проверку на работоспособность
#     not_added_count = 0 # Не прошел проверку на работоспособность
#     repeated_proxies = 0 # Дублирующийся прокси
#
#     # Собираем информацию из атрибута класса spy1x
#     tr_spy1x = soup.find_all('tr', class_='spy1x')
#     for tr in tr_spy1x:
#         font_spy14 = tr.find('font', class_='spy14')
#         if font_spy14:
#             ip = font_spy14.text.strip()
#             if check_proxy(ip):
#                 proxy_list.append(ip)
#                 added_count += 1
#                 print(f'IP-адрес {ip} добавлен в список! Всего добавлено - < {added_count} >')
#             else:
#                 not_added_count += 1
#                 print(f'Предупреждение: IP-адрес {ip} не работает и будет пропущен! Всего пропущено - < {not_added_count} >')
#
#     # Собираем информацию из атрибута класса spy1xx
#     tr_spy1xx = soup.find_all('tr', class_='spy1xx')
#     for tr in tr_spy1xx:
#         font_spy14 = tr.find('font', class_='spy14')
#         if font_spy14:
#             ip = font_spy14.text.strip()
#             if check_proxy(ip):
#                 if ip not in proxy_list: # Проверяем, есть ли уже такой IP в списке
#                     proxy_list.append(ip)
#                     added_count += 1
#                     print(f'IP-адрес {ip} добавлен в список! Всего добавлено - < {added_count} >')
#                 else:
#                     repeated_proxies += 1
#                     print(f'Предупреждение: IP-адрес {ip} уже существует и будет пропущен! Всего дублирующихся - < {repeated_proxies} >')
#             else:
#                 not_added_count += 1
#                 print(
#                     f'Предупреждение: IP-адрес {ip} не работает и будет пропущен! Всего пропущено - < {not_added_count} >')
#
#     if proxy_list: # Если список proxies не пустой - записывает значения в csv-файл
#         os.makedirs(csv_directory, exist_ok=True) # Создает директорию, в которую будет записан csv-файл
#         with open(csv_path, 'w', newline='', encoding='utf-8') as csvfile:
#             writer = csv.writer(csvfile)
#             writer.writerow(['IP Address'])
#             for ip in proxy_list:
#                 writer.writerow([ip])
#         print(f"IP-адреса успешно записаны в файл {csv_path}!")
#
#         # Выводит сообщение, уведомляющее о кол-ве валидных / невалидных прокси
#         print(f'Всего добавлено рабочих прокси - {added_count:5}!\n'
#               f'Всего дублирующихся прокси - {repeated_proxies:5}!\n'
#               f'Всего нерабочих прокси - {not_added_count:5}!\n'
#               f'Итого обработано прокси - {added_count + repeated_proxies + not_added_count:5}!\n')
#
#         # Подсчет времени, затраченного на обработку и проверку прокси
#         end_time = time.time()
#         elapsed_time = end_time - start_time
#         minutes = int(elapsed_time // 60)
#         seconds = int(elapsed_time % 60)
#         print(f'Всего затрачено времени: {minutes} минут и {seconds} секунд!')
#
#     else:
#         print("Не найдено IP-адресов, соответствующих шаблону.")
#
#
# def check_csv_directory_exists(csv_directory='csv_data'):
#     return os.path.isdir(csv_directory)
#
#
# def create_csv_directory(csv_directory='csv_data'):
#     os.makedirs(csv_directory, exist_ok=True)
#
#
# def save_csv_file(proxies, csv_directory='csv.data', csv_filename='proxies.csv'):
#     csv_path = os.path.join(csv_directory, csv_filename)
#     try:
#         with open(csv_path, 'w', newline='', encoding='utf-8') as csvfile:
#             writer = csv.writer(csvfile)
#             writer.writerow(['IP Address'])
#             for ip in proxies:
#                 writer.writerow([ip])
#         print(f"IP-адреса успешно записаны в файл {csv_path}!")
#     except Exception as e:
#         print(f'Ошибка записи в CSV-файл: {e}')
#         return []
#
#
# def check_proxy(ip):
#
#     try:
#         proxies = {
#             "http": f"socks5://{ip}",
#             "https": f"socks5://{ip}",
#         }
#         print(f'Отправляем запрос через SOCKS5, прокси: {ip}...')
#         response = requests.get("https://www.google.com", proxies=proxies, timeout=5)
#         print(f'Успешно! Код ответа: {response.status_code}')
#         if response.status_code == 200:
#             return True
#         else:
#             return False
#     except requests.exceptions.RequestException:
#         return False

if __name__ == "__main__":
    while True:
        url = url_from_user()  # Запрашиваем URL у пользователя
        if url is None:
            break  # Выход из цикла, если пользователь ввел 'exit'

        html_filename = url_to_filename(url)  # Получаем имя файла из URL
        if html_filename is None:
            print("Не удалось преобразовать URL в имя файла.")
            continue  # Переходим к следующей итерации цикла

        html_folder = 'html_data'  # Папка для HTML-файлов
        html_path = html_file_path(html_folder, html_filename)  # Путь к HTML-файлу

        csv_directory = 'csv_data'  # Папка для CSV-файлов
        csv_filename = html_filename.replace('.html', '.csv')  # Имя CSV-файла
        csv_path = html_file_path(csv_directory, csv_filename)  # Путь к CSV-файлу

        if not html_folder_exists(html_folder):  # Проверяем наличие папки для HTML
            if not create_html_folder(html_folder):  # Создаем папку, если ее нет
                continue  # Переходим к следующей итерации

        headers = generate_headers()  # Генерируем заголовки

        driver = initialize_stealth_webdriver(headers)  # Инициализируем драйвер
        if driver is None:
            print("Не удалось инициализировать драйвер.")
            continue  # Переходим к следующей итерации

        html = collect_html_code(url, driver, html_path, headers)  # Собираем HTML-код
        driver.quit()  # Закрываем драйвер



