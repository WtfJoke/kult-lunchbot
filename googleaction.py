"""
Handling Dialog of dialogflow.com used in Google Action
For more info about request/response
https://dialogflow.com/docs/fulfillment#request
https://dialogflow.com/docs/fulfillment#response
"""
import json
from flask import make_response, jsonify
import datetime
from lunchmenu import DateFormats
import scraper


class GoogleActionDialog:

    GOOGLE_LINE_SEPARATOR = "  "

    def __init__(self, request, kult_menu):
        self.request = request
        request_data = json.loads(request.data)
        self.request_result = request_data['result']
        self.kult_menu = kult_menu

    def handle(self):
        return self.handle_by_action()

    def handle_by_action(self):
        action = self.request_result['action']

        if action == "listMenus":
            response = self.action_list_menus()
        elif action == "selectedMenuNumber":
            response = self.action_selected_menu_number()
        elif action == "startAction":
            response = self.action_start()
        elif action == "whichMenu":
            response = self.action_which_menu()
        else:
            response = make_response('nothing to do here', 404)

        return response

    def action_list_menus(self):
        today = datetime.date.today()
        today_translated_weekday = today.strftime("%A") # TODO take date from request and change weekday to heute if weekday = heute
        daily_menu = self.kult_menu.get_daily_menu_by_date(today.strftime(DateFormats.COMMON))

        menu_count = len(daily_menu.get_menu_items())

        list_kult_menus = "Interessierst du dich für eine der {} Menüs die es {} im {} gibt?"\
            .format(menu_count, today_translated_weekday, "Kult")
        response = jsonify(speech=list_kult_menus,
                           displaytext=list_kult_menus,
                           source=scraper.URL)
        return make_response(response)

    def action_selected_menu_number(self):
        menu_numbers = self.request_result["parameters"]["number"]
        daily_menu = self.kult_menu.get_daily_menu_by_date(datetime.date.today().strftime(DateFormats.COMMON))
        menu_texts = []
        for menu_number in menu_numbers:
            if menu_number == 1:
                menu_texts.append(daily_menu.get_menu_one().get_menu())
            elif menu_number == 2:
                menu_texts.append(daily_menu.get_menu_two().get_menu())
            elif menu_number == 3:
                menu_texts.append(daily_menu.get_menu_three().get_menu())
            elif not menu_number: # empty string means all menus
                menu_texts.append(daily_menu.get_menu_one().get_menu())
                menu_texts.append(daily_menu.get_menu_two().get_menu())
                menu_texts.append(daily_menu.get_menu_three().get_menu())
            else:
                menu_texts.append("Sorry, habe kein Menü: " + str(menu_number))

        menu_text = self.GOOGLE_LINE_SEPARATOR.join(menu_texts)
        response = jsonify(speech=menu_text,
                           displaytext=menu_text,
                           source=scraper.URL)
        return make_response(response)

    def action_start(self):
        parameters = self.request_result["parameters"]
        date = parameters["date"]  # TODO: take session and remember all inputs like date
        list_restaurant_text = "Es gibt im Restaurant Kult Mittagstisch"
        response = jsonify(speech=list_restaurant_text,
                           displaytext=list_restaurant_text,
                           source=scraper.URL)
        return make_response(response)

    def action_which_menu(self):
        daily_menu = self.kult_menu.get_daily_menu_by_date(datetime.date.today().strftime(DateFormats.COMMON))
        menu_count = len(daily_menu.get_menu_items())
        which_menu_text = "Für welche der {} Menüs interessierst du dich?".format(menu_count)
        response = jsonify(speech=which_menu_text,
                           displaytext=which_menu_text,
                           source=scraper.URL)
        return make_response(response)


