from lunchmenu import WeeklyMenu, DailyMenu, MenuItem
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
from io import StringIO
import os
import re


def convert_pdf_to_txt(path):
    resource_manager = PDFResourceManager()
    try:
        with StringIO() as string_writer, open(path, 'rb') as pdf_file:
            device = create_text_converter(resource_manager, string_writer)
            interpreter = PDFPageInterpreter(resource_manager, device)

            for page in PDFPage.get_pages(pdf_file, maxpages=1):
                interpreter.process_page(page)

            pdf_text = string_writer.getvalue()
    finally:
        device.close()
    return pdf_text


def create_text_converter(resource_manager, string_writer):
    codec = 'utf-8'
    return TextConverter(resource_manager, string_writer, codec=codec, laparams=LAParams())


def get_menu_text(menu_filename):
    return str(get_menu(menu_filename))


def get_menu(menu_filename):
    pdf = os.path.join('menu', menu_filename)
    menu = analyze_menu_text(convert_pdf_to_txt(pdf), menu_filename)
    return menu


def analyze_menu_text(text, menu_filename):
    text_lines = text.split('\n')
    text_lines = list(filter(None, text_lines)) # filter empty values

    menu = WeeklyMenu(menu_filename)
    weekday = ''
    menu_number = 0
    menu_text = ''
    date = ''
    daily_menu = DailyMenu()

    for line in text_lines:
        if 'KW' in line:
            menu.set_title(line)
        elif any(item in line for item in WeeklyMenu.week_days):  # begins line with monday-friday
            match_day = re.compile('(\\w+)\\s(\\d\\d\.\\d\\d\\.\\d\\d\\d\\d)').match(line)  # match 'Montag 06.11.2017'
            if match_day:
                weekday = match_day.group(1)
                date = match_day.group(2)
                daily_menu.set_weekday(weekday)
                daily_menu.set_date(date)
        elif 'Menü' in line:
            menu_number = extract_menu_number(line)
            menu_text = line

            # TODO: decide whether menu_text should be complete line or just the food
            #replace_string = match_menu_line(line)
            #if replace_string: # menu X can be replaced, replace it
            #    menu_text = line.replace(replace_string.group(), '').strip()
            #else: # fallback
            #    menu_text = line

        if weekday and date and menu_number and menu_text:  # if all information present create menu item
            item = MenuItem(weekday, date, menu_number, menu_text)
            daily_menu.add_menu_item(item)
            menu_number = 0
            menu_text = ''

        if daily_menu.is_complete():
            menu.add_daily_menu(daily_menu)
            daily_menu = DailyMenu()

    return menu


def match_menu_line(menu_text_line):
    matcher = re.compile('Menü\\s(\\d)').match(menu_text_line)
    return matcher


def extract_menu_number(menu_text_line):
    menu_number = 0
    matcher = match_menu_line(menu_text_line)
    if matcher:
        menu_number = matcher.group(1)
    return menu_number

if __name__ == "__main__":
    print(get_menu_text('card.pdf'))