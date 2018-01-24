"""
Is responsible to fetch menus of external API for providing menues for "Restaurant Stiftsberg"
"""
import requests
import os
from configuration import Config
from datetime import datetime
from menu.weeklymenu import WeeklyMenu
from menu.dailymenu import DailyMenu
from menu.menuitem import MenuItem


class STIMenuFetcher:

    URL = "https://canteen.13.94.125.68.xip.io/api/"

    def get_token(self, username, password):
        start_time = datetime.now()

        payload = {'username': username, 'password': password}
        r = requests.post(self.URL + "token-auth/", data=payload, verify=False)

        self.measure_api_call("get_token", start_time)

        r.raise_for_status()
        response = r.json()
        return response['token']

    def get_menu_entries(self):
        start_time = datetime.now()

        auth_token = self.get_token(os.environ['STI_API_USER'], os.environ['STI_API_PASSWORD'])
        header = {"Authorization": "Token " + auth_token}
        # TODO: remove verify=False if API has proper ssl certificate
        r = requests.get(self.URL + "menuentries/", headers=header, verify=False)

        self.measure_api_call("get_menu_entries", start_time)
        r.raise_for_status()
        response = r.json()
        return response

    def get_menu_from_entries(self):
        response = self.get_menu_entries()
        weeklymenu = WeeklyMenu()
        dailymenu = DailyMenu()
        menuitem = MenuItem()
        dailymenu.set_date(None)

    @staticmethod
    def measure_api_call(method_name, start_time):
        time_elapsed = datetime.now() - start_time
        print(method_name + ' API-Request took (hh:mm:ss.ms) {}'.format(time_elapsed))


if __name__ == '__main__':
    Config.load_config()
    print(STIMenuFetcher().get_menu_from_entries())
