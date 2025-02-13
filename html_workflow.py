from collect_html import collect_html_code
from check_utils import html_file_exists


def start_or_skip_html_code_collection(html_filename, html_path, url, driver):
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
        print(f'\nЗапускаю обработку HTML-кода страницы под названием "{html_filename}"...')
    else:
        print(f'\nЗапускаю сбор HTML-кода страницы...')
        collect_html_code(url, driver, html_path)
        # if html_file:
        #     process_html_code()
        # else:
        #     print('Сбор HTML-кода не удался!')