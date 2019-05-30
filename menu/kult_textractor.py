import os
import re

from menu.dailymenu import KultDailyMenu
from menu.lunchmenu import WEEK_DAYS
from menu.menuitem import MenuItem
from menu.weeklymenu import KultWeeklyMenu
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
        menu = KultWeeklyMenu(menu_filename)

        next_weekday = next_date = ''
        daily_menu = KultDailyMenu()

        for positioned_text in text_lines:
            line = positioned_text.text

            if 'KW' in line:
                menu.set_title(line)
            elif any(item in line for item in WEEK_DAYS):  # begins line with monday-friday
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
            elif 'eschlossen' in line:
                daily_menu.set_weekday(next_weekday)
                daily_menu.set_date(next_date)
            elif 'Menü' in line:
                menu_number = KultTexTractor.extract_menu_number(line)
                positioned_text.text = KultTexTractor.remove_menu_prefix(line)

                item = MenuItem(daily_menu, '', menu_number)
                KultTexTractor.fill_menu_item(positioned_text, text_lines, item)

                daily_menu.add_menu_item(item)

                if daily_menu.is_complete():

                    menu.add_daily_menu(daily_menu)
                    daily_menu = KultDailyMenu()

                    if next_weekday or next_date:
                        daily_menu.set_weekday(next_weekday)
                        daily_menu.set_date(next_date)
                        next_weekday = ''
                        next_date = ''

        return menu

    @staticmethod
    def next_line_is_day(positioned_text, text_lines):
        next_positioned_text = KultTexTractor.get_next_line(positioned_text, text_lines)
        return any(item in next_positioned_text.text for item in WEEK_DAYS)

    @staticmethod
    def remove_menu_prefix(line):
        replace_string = KultTexTractor.match_menu_line(line)
        menu_text = ''
        if replace_string:  # menu X can be replaced, replace it
            menu_text = line.replace(replace_string.group(), '').strip()
        return menu_text

    @staticmethod
    def fill_menu_item(positioned_text, text_lines, menu_item):
        current_positioned_text = positioned_text
        # not menu and not begins line with monday-friday:
        while "Menü" not in current_positioned_text.text and not \
                any(item in current_positioned_text.text for item in WEEK_DAYS):

            if "Kl. Salat" in current_positioned_text.text:
                menu_item.set_salad(True)
                current_positioned_text.text = current_positioned_text.text \
                    .replace("Kl. Salat", "") \
                    .replace("|", "") \
                    .replace(" I ", " ").strip()

            if "Dessert" in current_positioned_text.text:
                menu_item.set_dessert(True)
                current_positioned_text.text = current_positioned_text.text \
                    .replace("IDessert", "") \
                    .replace("Dessert", "") \
                    .replace("|", "") \
                    .replace(" I ", " ").strip()

            is_price_match = re.compile('.*(\\d,\\d\\d).*').match(current_positioned_text.text)
            if is_price_match:
                price = is_price_match.group(1)
                menu_item.set_price(price)
                current_positioned_text.text = current_positioned_text.text.replace(price, "")

            is_friday_and_last_menu = menu_item.daily_menu.get_weekday() == WEEK_DAYS[4] and menu_item.menu_number == 3
            text_to_add = current_positioned_text.text.strip()
            menu_item.add_menu_text(current_positioned_text.text.strip())

            if is_friday_and_last_menu:  # stop reading bottom text like dailysoup
                break

            current_positioned_text = KultTexTractor.get_next_line(current_positioned_text, text_lines)

    @staticmethod
    def concat_menu_texts(menu_text, positioned_text, next_positioned_text, text_lines):
        while next_positioned_text.y_max == positioned_text.y_max:
            menu_text += " " + next_positioned_text.text.strip()
            positioned_text = next_positioned_text
            next_positioned_text = KultTexTractor.get_next_line(positioned_text, text_lines)
        return menu_text

    @staticmethod
    def extract_menu_text(line, next_line):
        menu_text = KultTexTractor.remove_menu_prefix(line)
        # if line is uncompleted and has menu on next line, take also next line
        if menu_text and next_line:
            menu_text += next_line
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

    @staticmethod
    def get_next_line(line, text_lines):
        counter = 0
        next_line = None

        while not next_line:
            counter = counter + 1
            line_counter = text_lines.index(line) + counter
            if len(text_lines) <= line_counter:
                break

            next_line = text_lines[line_counter]
        return next_line


# starter method
if __name__ == "__main__":
    import scraper

    pdf = scraper.get_pdf()
    current_menu = KultTexTractor.get_menu_from_pdf(pdf)
    print(current_menu)
