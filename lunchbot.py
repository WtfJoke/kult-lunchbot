import scraper
import pdf_textractor
import datetime
from lunchmenu import DateFormats

current_menu = None


def get_menu(date):
    menu = get_current_menu()
    daily_menu = menu.get_daily_menu_by_date(date)
    return get_menu_text(daily_menu, menu, date)


def get_menu_by_weekday(weekday):
    menu = get_current_menu()
    daily_menu = menu.get_daily_menu_by_weekday(weekday)
    return get_menu_text(daily_menu, menu, weekday)


def get_current_menu():
    if not current_menu:  # create menu if out of date or None
        create_menu()
    elif not current_menu.is_current(scraper.get_monday_date()):
        create_menu()
    return current_menu


def create_menu():
    pdf = scraper.get_pdf()
    global current_menu
    current_menu = pdf_textractor.get_menu(pdf)


def get_menu_text(daily_menu, menu, date):
    if daily_menu:
        menu_text = str(daily_menu)
    else:
        last_menu = menu.get_daily_menus()[len(menu.get_daily_menus()) - 1]
        if last_menu:
            menu_text = 'Sorry ich kann die Menüs von {} nicht finden'.format(str(date)) + '\n'
            menu_text += "Hier ist stattdessen das letzte Menü: \n\n"
            menu_text += str(last_menu)
        else:
            menu_text = "Fehler: Keine Menüs vorhanden"
    return menu_text


# starter method
if __name__ == "__main__":
    m = pdf_textractor.get_menu(scraper.get_pdf())
    today = datetime.date.today().strftime(DateFormats.FILE_FORMAT)
    d_menu = m.get_daily_menu_by_date(today)
    print(get_menu(datetime.date.today().strftime(DateFormats.COMMON)))



