import os


def check_csv_directory_exists(csv_directory='csv_data'):
    return os.path.isdir(csv_directory)


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
        print(f'\nФайл "{html_filename}" найден!')
        return True
    else:
        print(f'\nФайл "{html_filename}" не найден!')
        return False


def folder_exists(folder_name):
    """
    Проверяет наличие папки для хранения HTML-страниц.

    Аргументы:
        html_folder: Название папки для хранения HTML-страниц.

    Возвращает:
        True/False - папка найдена/папка не найдена.
    """
    if os.path.isdir(folder_name):
        print(f'\nПапка "{folder_name}" уже существует!')
        return True
    else:
        print(f'\nПапка "{folder_name}" не найдена!')
        return False


def csv_folder_exists(csv_folder):
    """
    Проверяет наличие папки для хранения HTML-страниц.

    Аргументы:
        html_folder: Название папки для хранения HTML-страниц.

    Возвращает:
        True/False - папка найдена/папка не найдена.
    """
    if os.path.isdir(csv_folder):
        print(f'Папка "{csv_folder}" найдена!')
        return True
    else:
        print(f'Папка "{csv_folder}" не найдена!')
        return False