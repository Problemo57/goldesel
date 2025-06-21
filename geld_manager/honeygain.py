from pathlib import Path
from datetime import datetime
from requests import get, post
from basic_source import BasicSource, Status
from os import environ


class Honeygain(BasicSource):
    honeygain_exchange = 1/1000
    payout_rate = 0.75

    def __init__(self):
        self.token = None
        if Path('honeygain_token').exists():
            self.token = Path('honeygain_token').read_text()

    def login(self):
        json_data = {
            "email": environ['HONEYGAIN_EMAIL'],
            "password": environ['HONEYGAIN_PASSWORD'],
        }

        response = post('https://dashboard.honeygain.com/api/v1/users/tokens', json=json_data)
        self.token = response.json()['data']['access_token']
        Path('honeygain_token').write_text(self.token)

    def get(self, url: str, params: dict = None):
        headers = {
            'Authorization': f'Bearer {self.token}',
        }
        response = get(url, params=params, headers=headers)
        if response.status_code != 200:
            self.login()
            headers = {
                'Authorization': f'Bearer {self.token}',
            }
            response = get(url, params=params, headers=headers)
            if response.status_code != 200:
                print(f"Error on get: {response.status_code}")
                raise Exception("Error on get")

        return response

    def get_status(self) -> Status:
        """Get the status of the source."""
        try:
            response = self.get('https://dashboard.honeygain.com/api/v2/devices')
            active_devices = [d for d in response.json()['data'] if d['status'] == 'active']
            my_device = [d for d in active_devices if d['model'] == environ['DEVICE_NAME']]
            if my_device:
                return Status.OK
            else:
                return Status.ERROR

        except Exception as e:
            print(f"Error on get_status: {e}")
            return Status.UNKNOWN

    def get_balance(self) -> float:
        """Get the total balance of the account."""
        try:
            response = self.get('https://dashboard.honeygain.com/api/v2/devices')
            my_device = [d for d in response.json()['data'] if d['model'] == environ['DEVICE_NAME']]
            return my_device[0]['stats']['total_credits'] * self.honeygain_exchange

        except Exception as e:
            print(f"Error on get_status: {e}")
            return 0

    def get_balance_today(self) -> float:
        """Get the balance earned today."""
        today = datetime.now().date().isoformat()
        params = {
            "date_from": today,
            "date_to": today,
        }

        try:
            response = self.get('https://dashboard.honeygain.com/api/v2/devices/activity', params=params)
            my_device = [d for d in response.json()['data'].values() if d['model'] == environ['DEVICE_NAME']][0]
            return my_device['stats'][today]['credits'] * self.honeygain_exchange

        except Exception as e:
            print(f"Error on get_balance_today: {e}")
            return 0

    def get_data_usage(self) -> int:
        """Get the total data usage statistics."""
        try:
            response = self.get('https://dashboard.honeygain.com/api/v2/devices')
            my_device = [d for d in response.json()['data'] if d['model'] == environ['DEVICE_NAME']]
            return my_device[0]['stats']['total_traffic']

        except Exception as e:
            print(f"Error on get_data_usage: {e}")
            return 0

    def get_data_usage_today(self) -> int:
        """Get the data usage statistics for today."""
        today = datetime.now().date().isoformat()
        params = {
            "date_from": today,
            "date_to": today,
        }

        try:
            response = self.get('https://dashboard.honeygain.com/api/v2/devices/activity', params=params)
            my_device = [d for d in response.json()['data'].values() if d['model'] == environ['DEVICE_NAME']][0]
            return my_device['stats'][today]['traffic']

        except Exception as e:
            print(f"Error on get_balance_today: {e}")
            return 0


if __name__ == '__main__':
    h = Honeygain()
    h.get_balance_today()
