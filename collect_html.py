import time

from file_utils import save_html_file
from webdriver_utils import click_button
from user_input import button_name_from_user, xpath_from_user


def collect_html_code(url: str, driver, html_path):
    """
    Используется для сбора необходимого HTML-кода с заданного URL-адреса.
    После получения HTML-страницы собирает все значения IP:Port и записывает их в csv-файл.

    После получения значения IP:Port при помощи функции check_proxy проверяет валидность полученных прокси.
    Проверка осуществляется при помощи get-запросов на сайт Google и только после получения положительного ответа
    на запрос IP:Port добавляется в список, после чего список сохраняется в csv-файл.
    """
    try:
        print('\nИнформация о первой кнопке:')
        button_name1 = button_name_from_user()
        if button_name1 is None:
            return None
        button_xpath1 = xpath_from_user()
        if button_xpath1 is None:
            return None

        print("\nИнформация о второй кнопке:")
        button_name2 = button_name_from_user()
        if button_name2 is None:
            return None
        button_xpath2 = xpath_from_user()
        if button_xpath2 is None:
            return None

        driver.get(url)
        time.sleep(3)

        if not click_button(driver, button_xpath=button_xpath1, button_name=button_name1):
            print(f'Ошибка нажатия кнопки "{button_name1}.')
            return None

        time.sleep(2)

        if not click_button(driver, button_xpath=button_xpath2, button_name=button_name2):
            print(f'Ошибка нажатия кнопки "{button_name2}.')
            return None

        html = driver.page_source

        if save_html_file(html, html_path):
            return html
        else:
            return None

    except (ConnectionError, TimeoutError) as e:
        print(f'Ошибка подключения к сайту: {e}')
        return None
    finally:
        if driver:
            driver.quit()