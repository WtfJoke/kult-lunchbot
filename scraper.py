from urllib.request import urlopen
from bs4 import BeautifulSoup, SoupStrainer


url = "http://wtz-tagungszentrum.de/restaurants/"
page = urlopen(url)

if page.status != 200:
    print('something wrong with url ' + url)

soup = BeautifulSoup(page,  "html.parser", parse_only=SoupStrainer('a'))
for link in soup:
    if link.has_attr('href'):
        target = link['href']
        if target.endswith('.pdf'):
            menu_card_link = target
            print(menu_card_link)