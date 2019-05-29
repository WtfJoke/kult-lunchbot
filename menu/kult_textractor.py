import os
import re
from datetime import datetime

from babel import Locale

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

        weekday = menu_text = date = next_weekday = next_date = ''
        daily_menu = KultDailyMenu()
        menu_number = 0

        for positioned_text in text_lines:
            line = positioned_text.text
            strippedLine = line.strip()
            next_positioned_text = KultTexTractor.get_next_line(positioned_text, text_lines)

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
                    # reset text if for some reasons more than 3 menus are red in one day
                    menu_text = ''
                    menu_number = 0
            elif 'eschlossen' in line:
                daily_menu.set_weekday(next_weekday)
                daily_menu.set_date(next_date)
            elif 'Menü' in line:
                menu_number = KultTexTractor.extract_menu_number(line)
                first_menu_text_line = KultTexTractor.remove_menu_prefix(line)
                uncompleted_line = strippedLine.endswith('|') or strippedLine.endswith('und') \
                                   or strippedLine.endswith('-')
                if uncompleted_line:
                    next_line = KultTexTractor.get_next_line(positioned_text, text_lines)

                    if next_line:
                        first_menu_text_line += " " + next_line.text.strip()
                menu_text = KultTexTractor.concat_menu_texts(first_menu_text_line, positioned_text,
                                                             next_positioned_text, text_lines)
                if not menu_text:  # text could be on previous lines
                    index = text_lines.index(positioned_text)
                    menu_text = text_lines[index - 2].text.strip() + " " + \
                                text_lines[index - 1].text.strip()

            elif menu_number and strippedLine and date and not menu_text:  # menu_text could be on next line - fallback
                # menu 3 text is some times at the end of document
                line = strippedLine
                weekday_number = datetime.strptime(date, "%d.%m.%Y").weekday()  # get translated week day
                date_weekday = Locale('de', 'DE').days['format']['wide'][weekday_number]

                if date_weekday == weekday:
                    menu_text = line

            if weekday and date and menu_number and menu_text:  # if all information present create menu item
                item = MenuItem(daily_menu, menu_text)
                daily_menu.add_menu_item(item)
                menu_number = 0
                menu_text = ''

                if daily_menu.is_complete():
                    menu.add_daily_menu(daily_menu)
                    date = ''
                    daily_menu = KultDailyMenu()

                    if next_weekday or next_date:
                        daily_menu.set_weekday(next_weekday)
                        daily_menu.set_date(next_date)
                        date = next_date
                        weekday = next_weekday
                        next_weekday = ''
                        next_date = ''

        return menu

    @staticmethod
    def remove_menu_prefix(line):
        replace_string = KultTexTractor.match_menu_line(line)
        menu_text = ''
        if replace_string:  # menu X can be replaced, replace it
            menu_text = line.replace(replace_string.group(), '').strip()
        return menu_text

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
        if menu_text and next_line:  # if line is uncompleted and has menu on next line, take also next line
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
