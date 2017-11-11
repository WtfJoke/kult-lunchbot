import scraper
import pdf_textractor
import datetime
import slack_sender


# starter method
if __name__ == "__main__":
    pdf = scraper.get_pdf()
    menu = pdf_textractor.get_menu(pdf)
    today = datetime.date.today().strftime('%d_%m')
    daily_menu = menu.get_daily_menu_by_date(today)
    if daily_menu:
        slack_sender.send_message(str(daily_menu))
        print(str(daily_menu))
    else:
        print('Sorry, cant get the daily menu of today: ' + datetime.date.today().strftime('%A %d.%m'))
        print('Here is the last available menu:')
        last_menu = menu.get_daily_menus()[len(menu.get_daily_menus()) - 1]
        print(str(last_menu))
        slack_sender.send_message(str(last_menu))

    # print(str(menu.get_daily_menu_by_weekday(Days.THURSDAY)))
    # print(str(menu.get_daily_menu_by_weekday(Days.MONDAY).get_menu_two()))
    # print(str(menu))