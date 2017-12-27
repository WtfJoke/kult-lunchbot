"""
Is responsible to fetch menus of external API for providing menues for "Restaurant Stiftsberg"
"""
import requests
import os
from configuration import Config


class STIMenuFetcher:

    URL = "https://canteen.13.94.125.68.xip.io/api/"

    def get_token(self, username, password):
        payload = {'username': username, 'password': password}
        # TODO: remove verify=False if API has proper ssl certificate
        r = requests.post(self.URL + "token-auth/", data=payload, verify=False)
        r.raise_for_status()
        response = r.json()
        return response['token']

    def get_menu_entries(self):
        auth_token = self.get_token(os.environ['STI_API_USER'], os.environ['STI_API_PASSWORD'])
        header = {"Authorization": "Token " + auth_token}
        # TODO: remove verify=False if API has proper ssl certificate
        r = requests.get(self.URL + "menuentries/", headers=header, verify=False)
        r.raise_for_status()
        response = r.json()
        print(response)


if __name__ == '__main__':
    Config.load_config()
    print(STIMenuFetcher().get_menu_entries())
