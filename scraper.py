from urllib.request import urlopen, urlretrieve, Request
from bs4 import BeautifulSoup, SoupStrainer
import datetime
import os
import logging
from menu.lunchmenu import DateFormats

URL = "http://wtz-tagungszentrum.de/restaurants/"


def get_pdf():
    create_menu_folder()
    file = get_menu_file()
    if not os.path.exists(file):
        download_pdf(file)
    return file


def extract_menu_card_link():
    logging.info("Crawl pdf")
    page = open_url()
    soup = BeautifulSoup(page, "html.parser", parse_only=SoupStrainer('a'))  # parse only links
    menu_card_link = None
    for link in soup:
        if link.has_attr('href'):
            target = link['href']
            if target.endswith('.pdf'):
                menu_card_link = target
                logging.info("Found pdf link: " + menu_card_link)
                break

    return menu_card_link


def open_url():
    r = Request(URL,
                headers={'User-Agent': "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:40.0) Gecko/20100101 Firefox/40.0"})
    page = urlopen(r)
    if page.status != 200:
        print('something wrong with url ' + URL)
        logging.error("Something wrong with url: " + URL)
        raise SystemError("Cant open URL: " + URL)
    return page


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
    file = os.path.join(get_menu_folder(), get_menu_file_name())
    return file


def get_monday_date():
    today = datetime.date.today()
    last_monday = today - datetime.timedelta(days=today.weekday())
    return last_monday.strftime(DateFormats.FILE_FORMAT)


def create_menu_folder():
    directory = get_menu_folder()
    if not os.path.exists(directory):
        os.makedirs(directory)


def get_menu_folder():
    project_root = os.path.dirname(os.path.realpath(__file__))
    return os.path.join(project_root, "resources", "menues")


# starter method
if __name__ == "__main__":
    logging.getLogger().setLevel(logging.DEBUG)
    get_pdf()
