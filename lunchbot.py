import scraper
import pdf_textractor
import datetime
import slack_sender


def get_menu(date=datetime.date.today().strftime('%d_%m')):
    pdf = scraper.get_pdf()
    menu = pdf_textractor.get_menu(pdf)
    daily_menu = menu.get_daily_menu_by_date(date)
    menu_text = ''
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
    pdf = scraper.get_pdf()
    menu = pdf_textractor.get_menu(pdf)
    today = datetime.date.today().strftime('%d_%m')
    daily_menu = menu.get_daily_menu_by_date(today)
    slack_sender.send_message(get_menu())



