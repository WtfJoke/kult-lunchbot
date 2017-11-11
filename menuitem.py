class MenuItem:

    week_days = ['Montag', 'Dienstag', 'Mittwoch', 'Donnerstag', 'Freitag']

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
