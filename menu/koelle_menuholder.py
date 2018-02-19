from menu.koelle_scraper import KoelleScraper
import datetime
from menu.lunchmenu import DateFormats

current_menu = None

def get_menu_text_by_date(date):
    menu = get_current_menu()
    daily_menu = menu.get_daily_menu_by_date(date)
    return get_menu_text(daily_menu, menu, date)


def get_menu_text_by_weekday(weekday):
    menu = get_current_menu()
    daily_menu = menu.get_daily_menu_by_weekday(weekday)
    return get_menu_text(daily_menu, menu, weekday)


def get_current_menu():
    if not current_menu or not current_menu.is_current(datetime.date.today()):  # create menu if out of date or None
        create_menu()
    return current_menu


def create_menu():
    global current_menu
    print("Creating new koelle menu object")
    current_menu = KoelleScraper.scrape()


def get_menu_text(daily_menu, menu, date):
    if daily_menu:
        menu_text = str(daily_menu)
    else:
        no_menus = len(menu.get_daily_menus()) == 0
        if no_menus:
            menu_text = "Fehler: Keine Menüs vorhanden"
        else:
            last_menu = menu.get_daily_menus()[len(menu.get_daily_menus()) - 1]
            menu_text = 'Sorry ich kann die Menüs von {} nicht finden'.format(str(date)) + '\n'
            menu_text += "Hier ist stattdessen das letzte Menü: \n\n"
            menu_text += str(last_menu)

    return menu_text


# starter method
if __name__ == "__main__":
    print(get_menu_text_by_date(datetime.date.today().strftime(DateFormats.COMMON)))



