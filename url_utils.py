import re



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
    try:
        match = re.search(r"//(?:www\.)?([^/]+)", url)
        if match:
            return match.group(1).split(".")[0]
        return url.split(".")[0]
    except (ValueError, AttributeError):
        print('Некорректный формат URL-адреса.')
        return None


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
        print(f'\nНе удалось преобразовать URL в имя файла.')
    else:
        print(f'\nНазвание вашего файла с HTML-страницей - "{html_filename}"! ')
        return html_filename

