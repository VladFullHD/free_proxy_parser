from functions import html_file_exists, html_folder_exists, url_from_user, url_to_filename, save_html_file
from functions import html_file_path, url_to_domain

if __name__ == '__main__':

    html_folder = 'html_data'
    url = url_from_user()
    html_filename = url_to_filename(url)
    html_path = html_file_path(html_folder, html_filename)
    save_html_file()