import datetime


class DateFormats:
    COMMON = "%d.%m.%Y"
    FILE_FORMAT = "%d_%m"


class WeeklyMenu:
    week_days = ['Montag', 'Dienstag', 'Mittwoch', 'Donnerstag', 'Freitag']

    def __init__(self, filename):
        self.daily_menus = []
        self.title = ''
        self.filename = filename

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

    def get_filename(self):
        return self.filename

    def is_current(self, last_monday_date):
        filename = "menu_" + last_monday_date + ".pdf"
        return filename == self.get_filename()

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
        self.weekday = weekday.strip()

    def get_date(self):
        return self.date

    def set_date(self, date):
        self.date = date

    def add_menu_item(self, menu_item):
        self.menus.append(menu_item)
        self.assign_to_menu_one_to_three(menu_item)

    def assign_to_menu_one_to_three(self, menu_item):
        number = menu_item.get_menu_number()
        if number == 1:
            self.menu1 = menu_item
        elif number == 2:
            self.menu2 = menu_item
        elif number == 3:
            self.menu3 = menu_item
        else:
            print('Menu unknown number' + str(menu_item))

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
        daily_menu += '\n'.join(str(item) for item in self.get_menu_items())
        return daily_menu


class MenuItem:

    PREFIX = "Menü "

    def __init__(self, daily_menu, menu_number, menu_text):
        self.daily_menu = daily_menu
        self.menu_number = int(menu_number)
        self.menu_text = menu_text

    def get_daily_menu(self):
        return self.daily_menu

    def get_menu_number(self):
        return self.menu_number

    def get_menu_content(self):
        return self.menu_text

    def get_menu(self):
        return self.PREFIX + str(self.menu_number) + " - " + self.menu_text

    def __str__(self):
        return self.get_menu()


class KeywordAnalyzer:

    FOOD = "essen"
    NAME = "kult"
    MENU = "menü"
    LUNCH = "mittag"

    def __init__(self, message):
        self.message = message.lower()
        self.triggers = False
        self.today = True
        self.relative_day = False
        self.day = ''
        self.date = datetime.date.today().strftime(DateFormats.COMMON)

    def analyze(self):
        self.triggers = self.trigger_word(self.FOOD) or self.trigger_word(self.NAME) or \
                        self.trigger_word(self.MENU) or self.trigger_word(self.LUNCH)
        if self.triggers:
            for day in WeeklyMenu.week_days:
                if day.lower() in self.message:
                    self.day = day
                    self.today = False
                    break
            for relative_day in RelativeDays.DAYS:
                if relative_day.get_keyword() in self.message:
                    self.today = False
                    self.relative_day = True
                    self.date = relative_day.get_date()
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

    def is_relative_day(self):
        return self.relative_day

    def get_day(self):
        return self.day

    def get_date(self):
        return self.date


class RelativeDay:

    def __init__(self, keyword, days_to_add):
        self.keyword = keyword
        self.days_to_add = days_to_add

    def get_keyword(self):
        return self.keyword

    def get_date(self):
        date = datetime.date.today() + datetime.timedelta(days=self.days_to_add)
        return date.strftime(DateFormats.COMMON)


class RelativeDays:
    TOMORROW = RelativeDay("morgen", 1)
    DAY_AFTER_TOMORROW = RelativeDay("übermorgen", 2)
    YESTERDAY = RelativeDay("gestern", -1)
    DAY_BEFORE_YESTERDAY = RelativeDay("vorgestern", -2)

    DAYS = [DAY_AFTER_TOMORROW, TOMORROW, DAY_BEFORE_YESTERDAY, YESTERDAY]