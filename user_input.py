import re

from file_utils import create_folder
from check_utils import folder_exists


def html_folder():
    folder = input('Введите название папки для сохранения HTML-страницы!:')
    return folder


def csv_folder():
    folder = input('Введите название папки для сохранения CSV-файла!')
    return folder


#def user_folder_name(folder):
    while True:
        folder = input('Введите название папки для сохранения HTML-страницы: ')
        if not folder:
            print('Название папки не может быть пустым!')
            continue
        print(f'Папка под названием "{folder}" успешно создана!')
        if not re.match(r'^[a-zA-Z0-9_/-]+$', folder):
            print('Название папки может содержать только буквы, цифры, подчеркивания и дефисы!')
            continue
        return folder


def user_folder_name_html():
    while True:
        print(f'\nВведите название папки для сохранения HTML-страницы! \nИли нажмите Enter для использования "html_data" в качестве названия:', end=' ')
        folder_name = input()

        if not folder_name:
            folder_name = 'html_data'

        if folder_exists(folder_name):
            print(f'\nИспользовать уже существующую папку? (y/n):', end=' ')
            answer = input().lower()
            if answer == 'y':
                return folder_name
            else:
                continue
        create_folder(folder_name)
        if not re.match(r'^[a-zA-Z0-9_/-]+$', folder_name):
            print('\nНазвание папки может содержать только буквы, цифры, подчеркивания и дефисы!')
            continue
        return folder_name


def user_folder_name_csv():
    while True:
        folder_name = input('Введите название папки для сохранения CSV-файла:')
        if not folder_name:
            print('Название папки не может быть пустым!')
            continue
        print(f'Папка под названием "{folder_name}" успешно создана!')
        if not re.match(r'^[a-zA-Z0-9_/-]+$', folder_name):
            print('Название папки может содержать только буквы, цифры, подчеркивания и дефисы!')
            continue
        return folder_name


def url_from_user():
    """
    Получает URL-адрес страницы от пользователя.
    """
    while True:
        try:
            url = input('Введите URL-адрес страницы в формате "https://www.example.com" или введите "exit" в консоль: ')
            if url.lower() == 'exit':
                return None

            if not re.match(r'^(https?://)', url):
                print('URL-адрес должен начинаться с "http://" или "https://"!')
                continue

            return url
        except KeyboardInterrupt:
            print('\nВы прервали ввод URL-адреса. Для выхода введите "exit".')
            continue



def csv_filename_from_user():
    while True:
        filename = input('Введите имя файла для сохранения CSV:')
        if not filename:
            print('Имя файла не может быть пустым!')
            continue
        return filename


def button_name_from_user():
    while True:
        button_name = input('Введите название кнопки, на которую должен нажать Selenium: ')
        if button_name.lower() == 'exit':
            return None
        if button_name:
            return button_name


def xpath_from_user():
    while True:
        button_xpath = input('Введите путь XPATH, который ведет к необходимой кнопке: ')
        if button_xpath.lower() == 'exit':
            return None
        if button_xpath:
            return button_xpath