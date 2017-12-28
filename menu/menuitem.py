class MenuItem:

    PREFIX = "Menü "

    def __init__(self, daily_menu, menu_number, menu_text):
        self.daily_menu = daily_menu
        self.menu_number = int(menu_number)
        self.menu_text = menu_text

    def get_daily_menu(self):
        return self.daily_menu

    def get_menu_number(self):
        return self.menu_number

    def get_menu_content(self):
        return self.menu_text

    def get_menu(self):
        return self.PREFIX + str(self.menu_number) + " - " + self.menu_text

    def __str__(self):
        return self.get_menu()
