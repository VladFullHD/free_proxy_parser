import requests
from bs4 import BeautifulSoup
import lxml
import time
import csv
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium_stealth import stealth



def get_free_proxy(url, filename='proxies.html', headers=None, output_filename='Proxies.csv'):

    # Проверяет, существует ли файл с HTML-страницей. Если да - переходит сразу к парсингу.
    if os.path.exists(filename):
        print(f'Файл {filename} найден. Запускаю парсинг...')
        with open(filename, 'r', encoding='utf-8') as f:
            html = f.read()
    else:
        print(f'Файл {filename} не найден. Запускаю браузер и выполняю работу по сбору кода HTML-страницы...')
        options = webdriver.ChromeOptions()


        # Проверяет, существует ли словарь headers и добавляет заголовки в options
        if headers:
            for key, value in headers.items():
                options.add_argument(f'--header={key}:{value}')

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

            driver.get(url)

            # try:
            #     # После загрузки необходимой страницы ищет определенный элемент.
            #     WebDriverWait(driver, 20).until(
            #         EC.presence_of_element_located((By.XPATH, '/html/body/table[2]/tbody/tr[4]/td/table/tbody/tr[3]/td[4]/a/font'))
            #     )
            #     time.sleep(5)
            # except:
            #     print('Элемент не найден за отведенное время.')
            #     return []

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
    proxies = []


    table = soup.find_all('font', class_='spy14')
    if table:
        for row in table:
            ip = row.text
            proxies.append(ip)

        with open(output_filename, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['IP Address'])
            for ip in proxies:
                writer.writerow([ip])
    else:
        print('Таблица с прокси не найдена. Проверьте структуру сайта.')
    return proxies


headers = {
        'accept': '*/*',
        'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36',
    }

if __name__ == '__main__':
    get_free_proxy('https://spys.one/en/socks-proxy-list/')