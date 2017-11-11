import scraper
import pdf_textractor
from lunchmenu import Days


# starter method
if __name__ == "__main__":
    pdf = scraper.get_pdf()
    menu = pdf_textractor.get_menu(pdf)
    print(str(menu.get_daily_menu(Days.THURSDAY)))
    print(str(menu.get_daily_menu(Days.MONDAY).get_menu_two()))
    print(str(menu))


    #menus.get_items_for(monday).getMenu1()