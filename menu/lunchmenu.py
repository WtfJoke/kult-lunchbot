import datetime

WEEK_DAYS = ['Montag', 'Dienstag', 'Mittwoch', 'Donnerstag', 'Freitag']


class DateFormats:
    COMMON = "%d.%m.%Y"
    FILE_FORMAT = "%d_%m"


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
            for day in WEEK_DAYS:
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