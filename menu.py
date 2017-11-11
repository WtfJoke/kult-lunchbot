class Menu:
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
