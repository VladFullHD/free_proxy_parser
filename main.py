from file_utils import html_file_path
from html_workflow import start_or_skip_html_code_collection
from url_utils import url_to_filename
from user_input import url_from_user, user_folder_name_html
from webdriver_utils import generate_headers, initialize_stealth_webdriver

if __name__ == "__main__":
    while True:
        url = url_from_user()  # Запрашиваем URL у пользователя
        if url is None:
            break  # Выход из цикла, если пользователь ввел 'exit'

        folder_name = user_folder_name_html()

        html_filename = url_to_filename(url)  # Получаем имя файла из URL

        html_path = html_file_path(folder_name, html_filename)  # Путь к HTML-файлу

        headers = generate_headers()

        driver = initialize_stealth_webdriver(headers)

        start_or_skip_html_code_collection(html_filename, html_path, url, driver)






'//*[@id="xpp"]'
'//*[@id="xpp"]'
'//*[@id="xpp"]/option[6]'

'https://spys.one/en/socks-proxy-list/'