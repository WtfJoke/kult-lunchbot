import re

from menu.lunchmenu import WEEK_DAYS
from menu.menuitem import MenuItem
from menu.dailymenu import DailyMenu
from menu.weeklymenu import WeeklyMenu


class KoelleTexTractor:

    DAY_DATE_PATTERN = re.compile("(\\w+),\\s(\\d\\d\.\\d\\d\\.\\d\\d\\d\\d)")

    def __init__(self):
        self.weeklymenu = WeeklyMenu()
        self.dailymenues = {}

    def weekly_menu(self):
        return self.weeklymenu

    def analyze_header(self, strong_tag):
        header = strong_tag.text

        if any(item in header for item in WEEK_DAYS):  # contains weekday
            match_day = self.DAY_DATE_PATTERN.match(header)  # match 'Montag, 17.02.2018'
            if match_day:
                weekday = match_day.group(1)
                date = match_day.group(2)
                self.create_daily_menu_with_date(header, date, weekday)
        # TODO: parse vegan weekly special header

    def create_menu_entry(self, header, menu_text):
        daily = self.dailymenues[header]
        daily.add_menu_item(MenuItem(daily, menu_text))

    def determine_header_to_read(self, existing_header_to_read, text):
        header_to_read = existing_header_to_read
        if text in self.dailymenues:
            header_to_read = text
        elif text:
            header_to_read = None
        return header_to_read

    def create_daily_menu_with_date(self, header, date, weekday):
        daily_menu = DailyMenu()
        daily_menu.set_date(date)
        daily_menu.set_weekday(weekday)
        self.dailymenues[header] = daily_menu
        self.weeklymenu.add_daily_menu(daily_menu)
