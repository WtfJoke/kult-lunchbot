from bs4 import BeautifulSoup
from bs4 import Tag
from bs4 import NavigableString
from menu.koelle_textractor import KoelleTexTractor
from PyQt5.QtWebEngineWidgets import QWebEnginePage
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QUrl
import sys


class Page(QWebEnginePage):
    def __init__(self, url):
        self.app = QApplication(sys.argv)
        QWebEnginePage.__init__(self)
        self.html = ''
        self.loadFinished.connect(self._on_load_finished)
        self.load(QUrl(url))
        self.app.exec_()

    def _on_load_finished(self):
        self.html = self.toHtml(self.callable)
        print('Load finished')

    def callable(self, html_str):
        self.html = html_str
        self.app.quit()


class KoelleScraper:

    URL = 'https://www.pflanzen-koelle.de/standorte/heilbronn/bambusgarten/'

    @staticmethod
    def scrape():
        page = Page(KoelleScraper.URL)
        html = page.html

        extractor = KoelleTexTractor()
        soup = BeautifulSoup(html, "html.parser")

        p = soup.find_all('p', style="text-align: center;", limit=2)
        header = p[0]
        # wok_content = p[1]
        content = header

        extractor.weekly_menu().set_title(header.find('strong').text)
        KoelleScraper.find_menu_headers(content, extractor)
        KoelleScraper.find_menu_content(content, extractor)
        return extractor.weekly_menu()

    @staticmethod
    def find_menu_content(content, extractor):
        header = None
        for child in content.children:
            if isinstance(child, Tag):
                header = extractor.determine_header_to_read(header, child.text)
            elif header and isinstance(child, NavigableString):
                extractor.create_menu_entry(header, child)

    @staticmethod
    def find_menu_headers(content, extractor):
        for strong_tag in content.find_all('strong'):
            extractor.analyze_header(strong_tag)


if __name__ == "__main__":
    scraped_menu = KoelleScraper().scrape()
    print(str(scraped_menu))
