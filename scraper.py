from urllib.request import urlopen, urlretrieve
from bs4 import BeautifulSoup, SoupStrainer
import datetime
import os

URL = "http://wtz-tagungszentrum.de/restaurants/"


def get_pdf():
    return download_pdf(extract_menu_card_link())


def extract_menu_card_link():
    page = urlopen(URL)

    if page.status != 200:
        print('something wrong with url ' + URL)

    soup = BeautifulSoup(page,  "html.parser", parse_only=SoupStrainer('a'))
    menu_card_link = ''
    for link in soup:
        if link.has_attr('href'):
            target = link['href']
            if target.endswith('.pdf'):
                menu_card_link = target

    return menu_card_link


def download_pdf(link_to_pdf):
    filename = get_menu_file_name()
    file = get_menu_file()
    if not os.path.exists(file):
        print('Downloading pdf from ' + link_to_pdf)
        result = urlretrieve(link_to_pdf, file)
        # TODO: Better exception handling
    return filename


def get_menu_file_name():
    last_monday = get_monday_date()
    filename = 'menu_' + last_monday + '.pdf'
    return filename


def get_menu_file():
    file = os.path.join('menu', get_menu_file_name())
    return file


def get_monday_date():
    today = datetime.date.today()
    last_monday = today - datetime.timedelta(days=today.weekday())
    return last_monday.strftime('%d_%m')

# starter method
if __name__ == "__main__":
    get_pdf()