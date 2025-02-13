import os



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


def html_file_path(folder_name, html_filename):
    """
    Объединяет наименование папки для хранения HTML-страниц и наименование файла с HTML-страницей.
    Тем самым создает путь к необходимому нам файлу.

    Аргументы:
        html_folder: Название папки для хранения HTML-страниц.
        html_filename: Название файла с HTML-страницей.

    Возвращает:
        Путь к необходимому нам файлу.
    """
    return os.path.join(folder_name, html_filename)


def create_folder(folder_name):
    """
    Создает папку с определенным названием.

    Аргументы:
        html_folder: Наименование папки.

    Возвращает:
        True/False - папка успешно создана/произошла ошибка при создании папки.
    """
    try:
        os.makedirs(folder_name, exist_ok=True)
        print(f'\nПапка под названием "{folder_name}" успешно создана!')
        return True
    except Exception as e:
        print(f'\nПроизошла ошибка при создании папки "{folder_name}": {e}')
        return False









