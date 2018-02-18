from bs4 import BeautifulSoup
from bs4 import Tag
from bs4 import NavigableString
from menu.koelle_textractor import KoelleTexTractor
import scraper


class KoelleScraper:

    URL = 'https://www.pflanzen-koelle.de/standorte/heilbronn/bambusgarten/'

    @staticmethod
    def scrape():
        page = scraper.open_url(KoelleScraper.URL)

        extractor = KoelleTexTractor()
        soup = BeautifulSoup(page, "html.parser")
        content = soup.find('p', style="text-align: center;")

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
        for index, strong_tag in enumerate(content.find_all('strong')):
            if index == 0:
                extractor.weekly_menu().set_title(strong_tag.text)
            else:
                extractor.analyze_header(strong_tag)


if __name__ == "__main__":
    scraped_menu = KoelleScraper().scrape()
    print(str(scraped_menu))
