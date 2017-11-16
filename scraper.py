from urllib.request import urlopen, urlretrieve, Request
from bs4 import BeautifulSoup, SoupStrainer
import datetime
import os
import logging

URL = "http://wtz-tagungszentrum.de/restaurants/"


def get_pdf():
    file = get_menu_file()
    if not os.path.exists(file):
        download_pdf(file)

    return get_menu_file_name()


def extract_menu_card_link():
    logging.info("Crawl pdf")
    r = Request(URL, headers={'User-Agent': "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:40.0) Gecko/20100101 Firefox/40.0"})
    page = urlopen(r)
    if page.status != 200:
        print('something wrong with url ' + URL)
        logging.error("Something wrong with url: " + URL)

    soup = BeautifulSoup(page,  "html.parser", parse_only=SoupStrainer('a'))
    menu_card_link = ''
    for link in soup:
        if link.has_attr('href'):
            target = link['href']
            if target.endswith('.pdf'):
                menu_card_link = target
                logging.info("Found pdf link: " + menu_card_link)
                break

    return menu_card_link


def download_pdf(file):
    link_to_pdf = extract_menu_card_link()
    logging.info("Download pdf from " + link_to_pdf)
    result = urlretrieve(link_to_pdf, file)
    # TODO: Better exception handling


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
    logging.getLogger().setLevel(logging.DEBUG)
    get_pdf()