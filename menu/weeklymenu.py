import datetime
from menu.lunchmenu import DateFormats


class WeeklyMenu:

    def __init__(self):
        self.daily_menus = []
        self.title = ''
        self.from_date = datetime.date.today()
        self.to_date = self.from_date + datetime.timedelta(days=6) # usually valid for whole week

    def add_daily_menu(self, daily_menu):
        self.daily_menus.append(daily_menu)

    def get_daily_menus(self):
        return self.daily_menus

    def get_daily_menu_by_weekday(self, weekday):
        for daily_menu in self.get_daily_menus():
            if daily_menu.get_weekday() == weekday:
                return daily_menu
        return None

    def get_daily_menu_by_date(self, date=datetime.date.today().strftime(DateFormats.COMMON)):
        for daily_menu in self.get_daily_menus():
            if daily_menu.get_date() == date:
                return daily_menu
        return None

    def get_title(self):
        return self.title

    def set_title(self, title):
        self.title = title.strip()

    def is_current(self, today):
        return today <= self.to_date

    def __str__(self):
        menu_string = self.title + '\n'

        for daily_menu in self.get_daily_menus():
            menu_string += str(daily_menu) + '\n'

        return menu_string


class KultWeeklyMenu(WeeklyMenu):

    def __init__(self, filename):
        super().__init__()
        self.filename = filename

    def get_filename(self):
        return self.filename

    def is_current(self, last_monday_date):
        filename = "menu_" + last_monday_date + ".pdf"
        return filename == self.get_filename()



