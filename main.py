import requests
from bs4 import BeautifulSoup
import time
import csv
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium_stealth import stealth


def get_free_proxy(url, filename='proxies.html', headers=None, output_filename='proxies.csv'):
    """
    Используется для сбора необходимого HTML-кода с заданного URL-адреса.
    После получения HTML-страницы собирает все значения IP:Port и записывает их в csv-файл.

    После получения значения IP:Port при помощи функции check_proxy проверяет валидность полученных прокси.
    Проверка осуществляется при помощи get-запросов на сайт Google и только после получения положительного ответа
    на запрос IP:Port добавляется в список, после чего список сохраняется в csv-файл.
    """

    # Проверяет, существует ли файл с HTML-страницей. Если да - переходит сразу к парсингу.
    if os.path.exists(filename):
        print(f'Файл {filename} найден. Запускаю парсинг...')
    else:
        print(f'Файл {filename} не найден. Запускаю браузер и выполняю работу по сбору кода HTML-страницы...')
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
                with open(filename, 'w', encoding='utf-8') as f:
                    f.write(html)
            except Exception as e:
                print(f'Ошибка записи в файл: {e}')
                return []
        except Exception as e:
            print(f'Произошла ошибка Selenium: {e}')

        finally:
            if driver is not None:
                driver.quit()

    # Открывает сохраненную HTML-страницу и записывает в переменную для дальнейшей передачи в объект BeautifulSoup
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            html = f.read()
    except FileNotFoundError:
        print(f'Файл {filename} не найден.')
        return

    # Создает объект BeautifulSoup из полученной HTML-страницы для дальнейшей обработки данных
    soup = BeautifulSoup(html, 'lxml')

    # Запускает таймер для подсчета времени, затраченного на обработку и проверку прокси
    start_time = time.time()

    # Список с прокси, которые прошли проверку на валидность
    proxies = []

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
                proxies.append(ip)
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
                if ip not in proxies: # Проверяем, есть ли уже такой IP в списке
                    proxies.append(ip)
                    added_count += 1
                    print(f'IP-адрес {ip} добавлен в список! Всего добавлено < {added_count} >')
                else:
                    repeated_proxies += 1
                    print(f'Предупреждение: IP-адрес {ip} уже существует и будет пропущен! Всего дублирующихся - < {repeated_proxies} >')
            else:
                not_added_count += 1
                print(
                    f'Предупреждение: IP-адрес {ip} не работает и будет пропущен! Всего пропущено - < {not_added_count} >')

    if proxies: # Если список proxies не пустой - записываем значения в csv-файл
        with open(output_filename, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['IP Address'])
            for ip in proxies:
                writer.writerow([ip])
        print(f"IP-адреса успешно записаны в файл {output_filename}!")

        # Выводит сообщение, уведомляющее о кол-ве валидных / невалидных прокси
        print(f'Всего добавлено рабочих прокси = {added_count:5}!\n'
              f'Всего дублирующихся прокси = {repeated_proxies:5}!\n'
              f'Всего нерабочих прокси = {not_added_count:5}!\n'
              f'Итого обработано прокси = {added_count + repeated_proxies + not_added_count:5}!\n')

        # Подсчет времени, затраченного на обработку и проверку прокси
        end_time = time.time()
        elapsed_time = end_time - start_time
        minutes = int(elapsed_time // 60)
        seconds = int(elapsed_time % 60)
        print(f'Всего затрачено времени: {minutes} минут и {seconds} секунд!')

    else:
        print("Не найдено IP-адресов, соответствующих шаблону.")


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

if __name__ == '__main__':
    get_free_proxy('https://spys.one/en/socks-proxy-list/', headers=headers)

