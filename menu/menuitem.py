class MenuItem:

    PREFIX = "Menü "

    def __init__(self, daily_menu, menu_text, menu_number = None):
        self.daily_menu = daily_menu
        if menu_number:
            self.menu_number = int(menu_number)
        else:
            self.menu_number = len(self.daily_menu.get_menu_items()) + 1
        self.menu_text = menu_text
        self.has_dessert = False
        self.has_salad = False
        self.price = 0

    def get_daily_menu(self):
        return self.daily_menu

    def get_menu_number(self):
        return self.menu_number

    def get_menu_content(self):
        return self.menu_text

    def get_menu(self):
        return self.PREFIX + str(self.menu_number) + " - " + self.menu_text

    def has_dessert(self):
        return self.has_dessert

    def set_dessert(self, has_dessert):
        self.has_dessert = has_dessert

    def has_salad(self):
        return self.has_salad

    def set_salad(self, has_salad):
        self.has_salad = has_salad

    def set_price(self, price):
        self.price = price

    def add_menu_text(self, menu_text_to_add):
        self.menu_text += "" + menu_text_to_add

    def __str__(self):
        return self.get_menu()
