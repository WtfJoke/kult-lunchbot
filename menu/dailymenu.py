class DailyMenu:
    def __init__(self):
        self.weekday = ''
        self.date = ''
        self.menus = []

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

    def get_menu_items(self):
        return self.menus

    # Overwrite when all daily menus from that day are inserted
    def is_complete(self):
        return False

    def __str__(self):
        daily_menu = self.weekday + ' - ' + self.date + '\n'
        daily_menu += '\n'.join(str(item) for item in self.get_menu_items())
        return daily_menu


class KultDailyMenu(DailyMenu):
    def __init__(self):
        super().__init__()
        self.menu1 = None
        self.menu2 = None
        self.menu3 = None

    def add_menu_item(self, menu_item):
        super().add_menu_item(menu_item)
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

    def get_menu_one(self):
        return self.menu1

    def get_menu_two(self):
        return self.menu2

    def get_menu_three(self):
        return self.menu3

    def is_complete(self):
        return self.menu1 is not None and self.menu2 is not None and self.menu3 is not None
