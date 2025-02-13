import time
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium_stealth import stealth
from fake_useragent import UserAgent
from selenium import webdriver



def generate_headers():
    headers = {}

    ua = UserAgent()
    headers['User-Agent'] = ua.random

    return headers


def headers_to_options(options, headers):
    for key, value in headers.items():
        options.add_argument(f'--header={key}:{value}')


def initialize_stealth_webdriver(headers):
    """
    Создает экземпляр веб-драйвера с заданными опциями и применяет к нему stealth для скрытия факта использования Selenium

    Аргументы:
        headers: Словарь с заголовками. По умолчанию None.
    """
    options = webdriver.ChromeOptions()
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
                user_agent=headers['User-Agent']
                )
        return driver
    except Exception as e:
        print(f'Ошибка инициализации драйвера: {e}')
        return None


def click_button(driver, button_xpath, button_name):
    try:
        button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, button_xpath)))
        button.click()
        time.sleep(3)
    except:
        print(f'{button_name} кнопка не найдена!')
        return False
    return True