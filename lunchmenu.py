from enum import Enum


class WeeklyMenu:
    week_days = ['Montag', 'Dienstag', 'Mittwoch', 'Donnerstag', 'Freitag']

    def __init__(self):
        self.items = []
        self.daily_menus = []
        self.title = ''

    def add_menu_item(self, item):
        self.items.append(item)

    def add_daily_menu(self, daily_menu):
        self.daily_menus.append(daily_menu)

    def get_daily_menus(self):
        return self.daily_menus

    def get_daily_menu_by_weekday(self, weekday):
        for daily_menu in self.get_daily_menus():
            if daily_menu.get_weekday() == weekday:
                return daily_menu
        return None

    def get_daily_menu_by_date(self, date):
        for daily_menu in self.get_daily_menus():
            if daily_menu.get_date() == date:
                return daily_menu
        return None

    def get_items(self):
        return self.items

    def get_title(self):
        return self.title

    def set_title(self, title):
        self.title = title

    def __str__(self):
        menu_string = self.title + '\n'

        for daily_menu in self.get_daily_menus():
            menu_string += str(daily_menu) + '\n'

        return menu_string


class DailyMenu:
    def __init__(self):
        self.weekday = ''
        self.date = ''
        self.menus = []
        self.menu1 = None
        self.menu2 = None
        self.menu3 = None

    def get_weekday(self):
        return self.weekday

    def set_weekday(self, weekday):
        self.weekday = weekday

    def get_date(self):
        return self.date

    def set_date(self, date):
        self.date = date

    def add_menu_item(self, menu_item):
        number = menu_item.get_menu_number()
        if number == 1:
            self.menu1 = menu_item
        elif number == 2:
            self.menu2 = menu_item
        elif number == 3:
            self.menu3 = menu_item
        else:
            print('Menu unknown number' + str(menu_item))

        self.menus.append(menu_item)

    def get_menu_items(self):
        return self.menus

    def get_menu_one(self):
        return self.menu1

    def get_menu_two(self):
        return self.menu2

    def get_menu_three(self):
        return self.menu3

    def is_complete(self):
        return len(self.menus) == 3

    def __str__(self):
        daily_menu = self.weekday + ' - ' + self.date + '\n'
        daily_menu += self.get_menu_one().get_menu() + '\n'
        daily_menu += self.get_menu_two().get_menu() + '\n'
        daily_menu += self.get_menu_three().get_menu() + '\n'

        return daily_menu


class MenuItem:

    def __init__(self, weekday, date, menu_number, menu_text):
        self.weekday = weekday.strip()
        self.date = date
        self.menu_number = int(menu_number)
        self.menu_text = menu_text

    def get_week_day(self):
        return self.weekday

    def get_date(self):
        return self.date

    def get_menu_number(self):
        return self.menu_number

    def get_menu(self):
        return self.menu_text

    def __str__(self):
        return self.weekday + ' - ' + self.menu_text


class KeywordAnalyzer:

    FOOD = "essen"
    NAME = "kult"

    def __init__(self, message):
        self.message = message.lower()
        self.triggers = False
        self.today = True
        self.day = ''

    def analyze(self):
        self.triggers = self.trigger_word(self.FOOD) or self.trigger_word(self.NAME)
        if self.triggers:
            for day in WeeklyMenu.week_days:
                if day.lower() in self.message:
                    self.day = day
                    self.today = False
                    break
        return self

    def trigger_word(self, keyword):
        return self.message.startswith(keyword) or \
               self.message.endswith(keyword) or \
               ' ' + keyword in self.message

    def is_triggered(self):
        return self.triggers

    def is_today(self):
        return self.today

    def get_day(self):
        return self.day
