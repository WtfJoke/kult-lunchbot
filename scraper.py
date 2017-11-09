from urllib.request import urlopen
from bs4 import BeautifulSoup, SoupStrainer


URL = "http://wtz-tagungszentrum.de/restaurants/"


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


# starter method
if __name__ == "__main__":
    print(extract_menu_card_link())