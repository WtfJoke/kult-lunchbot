import os
import re

from lunchmenu import WeeklyMenu, DailyMenu, MenuItem
from pdf_textractor import convert_pdf_to_txt_lines


class KultTexTractor:

    DAY_DATE_PATTERN = re.compile("(\\w+)\\s(\\d\\d\.\\d\\d\\.\\d\\d\\d\\d)")

    @staticmethod
    def get_menu_text(menu_filename):
        return str(KultTexTractor.get_menu(menu_filename))

    @staticmethod
    def get_menu_from_pdf(pdf):
        menu = KultTexTractor.analyze_menu_text(convert_pdf_to_txt_lines(pdf), os.path.basename(pdf))
        return menu

    @staticmethod
    def analyze_menu_text(text_lines, menu_filename):
        menu = WeeklyMenu(menu_filename)

        weekday = menu_text = date = next_weekday = next_date = ''
        daily_menu = DailyMenu()
        menu_number = 0

        for line in text_lines:
            if 'KW' in line:
                menu.set_title(line)
            elif any(item in line for item in WeeklyMenu.week_days):  # begins line with monday-friday
                match_day = KultTexTractor.DAY_DATE_PATTERN.match(line)  # match 'Montag 06.11.2017'
                if match_day:
                    if not daily_menu.get_date():
                        weekday = match_day.group(1)
                        date = match_day.group(2)
                        daily_menu.set_weekday(weekday)
                        daily_menu.set_date(date)
                    else:
                        next_weekday = match_day.group(1)
                        next_date = match_day.group(2)
            elif 'Menü' in line:
                menu_number = KultTexTractor.extract_menu_number(line)
                menu_text = KultTexTractor.extract_menu_text(line)
            elif menu_number and line.strip() and not menu_text:  # menu_text could be on next line - fallback
                menu_text = line.strip()

            if weekday and date and menu_number and menu_text:  # if all information present create menu item
                item = MenuItem(daily_menu, menu_number, menu_text)
                daily_menu.add_menu_item(item)
                menu_number = 0
                menu_text = ''

                if daily_menu.is_complete():
                    menu.add_daily_menu(daily_menu)
                    date = ''
                    daily_menu = DailyMenu()

                    if next_weekday or next_date:
                        daily_menu.set_weekday(next_weekday)
                        daily_menu.set_date(next_date)
                        date = next_date
                        weekday = next_weekday
                        next_weekday = ''
                        next_date = ''

        return menu

    @staticmethod
    def extract_menu_text(line):
        replace_string = KultTexTractor.match_menu_line(line)
        if replace_string:  # menu X can be replaced, replace it
            menu_text = line.replace(replace_string.group(), '').strip()
        else:  # fallback
            menu_text = line
        return menu_text

    @staticmethod
    def match_menu_line(menu_text_line):
        matcher = re.compile('Menü\\s(\\d)').match(menu_text_line)
        return matcher

    @staticmethod
    def extract_menu_number(menu_text_line):
        menu_number = 0
        matcher = KultTexTractor.match_menu_line(menu_text_line)
        if matcher:
            menu_number = matcher.group(1)
        return menu_number