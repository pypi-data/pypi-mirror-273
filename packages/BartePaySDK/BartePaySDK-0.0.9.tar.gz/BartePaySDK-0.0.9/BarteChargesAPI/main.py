import requests

class BarteChargesAPI:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = 'https://api2.barte.com/v2/charges'

    def get_charge(self, charge_uuid):
        headers = {
            'X-Token-Api': self.api_key
        }
        url = f"{self.base_url}/{charge_uuid}"
        response = requests.get(url, headers=headers)
        return response.json()