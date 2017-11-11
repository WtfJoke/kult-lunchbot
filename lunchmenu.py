class WeeklyMenu:
    week_days = ['Montag', 'Dienstag', 'Mittwoch', 'Donnerstag', 'Freitag']

    def __init__(self):
        self.items = []
        self.title = ''

    def add_menu_item(self, item):
        self.items.append(item)

    def get_items(self):
        return self.items

    def get_title(self):
        return self.title

    def set_title(self, title):
        self.title = title

    def __str__(self):
        menu_string = self.title + '\n'

        for counter, item in enumerate(self.get_items()): # iterate with counter
            if counter % 3 == 0: # each third line
                menu_string += item.get_week_day() + '\n'
            menu_string += item.get_menu() + '\n'

        return menu_string


class DailyMenu:
    def __init__(self, weekday, date):
        self.weekday = weekday
        self.date = date


class MenuItem:



    def __init__(self, weekday, menu_number, menu_text):
        self.weekday = weekday
        self.menu_number = menu_number
        self.menu_text = menu_text

    def get_week_day(self):
        return self.weekday

    def get_menu_number(self):
        return self.menu_number

    def get_menu(self):
        return self.menu_text

    def __str__(self):
        return self.weekday + ' - ' + self.menu_text
