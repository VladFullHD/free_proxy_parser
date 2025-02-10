from functions import html_file_exists, html_folder_exists, url_from_user, url_to_filename
from functions import html_file_path

if __name__ == '__main__':

    html_folder = 'html_data'
    html_filename = 'proxies.html'
    html_path = html_file_path(html_folder, html_filename)
    url_from_user()
