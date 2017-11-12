import scraper
import pdf_textractor
import datetime
import slack_sender


# TODO - performance improve - extract text on each call - save extracted text
def get_menu(date=datetime.date.today().strftime('%d_%m')):
    pdf = scraper.get_pdf()
    menu = pdf_textractor.get_menu(pdf)
    daily_menu = menu.get_daily_menu_by_date(date)
    return get_menu_text(daily_menu, menu, date)


def get_menu_by_weekday(weekday):
    pdf = scraper.get_pdf()
    menu = pdf_textractor.get_menu(pdf)
    daily_menu = menu.get_daily_menu_by_weekday(weekday)
    return get_menu_text(daily_menu, menu, weekday)


def get_menu_text(daily_menu, menu, date):
    if daily_menu:
        menu_text = str(daily_menu)
    else:
        last_menu = menu.get_daily_menus()[len(menu.get_daily_menus()) - 1]
        if last_menu:
            menu_text = 'Sorry ich kann die Menüs von {} nicht finden'.format(str(date)) + '\n'
            menu_text += "Hier ist das stattdessen das letzte Menü: \n"
            menu_text += str(last_menu)
        else:
            menu_text = "Fehler: Keine Menüs vorhanden"
    return menu_text


# starter method
if __name__ == "__main__":
    m = pdf_textractor.get_menu(scraper.get_pdf())
    today = datetime.date.today().strftime('%d_%m')
    d_menu = m.get_daily_menu_by_date(today)
    slack_sender.send_message(get_menu())



