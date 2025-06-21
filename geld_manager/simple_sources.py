from os import environ
from requests import post, get
from pathlib import Path
from basic_source import BasicSource, Status


class Pawns(BasicSource):
    var_name = "pawns-cli"
    network_exchange = 0.20 / 1_000_000_000
    payout_rate = 0.96

    def __init__(self):
        self.token = None
        if Path('pawns_token').exists():
            self.token = Path('pawns_token').read_text()

    def login(self):
        json_data = {
            'email': environ['PAWNS_EMAIL'],
            'password': environ['PAWNS_PASSWORD'],
        }

        response = post('https://api.pawns.app/api/v1/users/tokens', json=json_data)
        self.token = response.json()['access_token']
        Path('pawns_token').write_text(self.token)

    def get_status(self) -> Status:
        if self.token is None:
            self.login()

        headers = {
            'authorization': f'Bearer {self.token}',
        }
        params = {
            'page': '1',
            'items_per_page': '20',
        }
        response = get('https://api.pawns.app/api/v1/users/me/devices', params=params, headers=headers)
        if response.status_code == 401:
            self.login()
            headers = {
                'authorization': f'Bearer {self.token}',
            }
            response = get('https://api.pawns.app/api/v1/users/me/devices', params=params, headers=headers)

        devices = response.json()['data']
        my_device = [d for d in devices if d['title'] == environ['DEVICE_NAME']]
        if not my_device:
            return Status.ERROR

        return Status.OK


# EarnApp (Simulierte Klasse)
class EarnApp(BasicSource):
    var_name = "earnapp"
    network_exchange = 0.10 / 1_000_000_000
    payout_rate = 0.98


# PacketStream (Simulierte Klasse)
class PacketStream(BasicSource):
    var_name = "psclient"
    network_exchange = 0.10 / 1_000_000_000
    payout_rate = 0.97


# Traffmonetizer (Simulierte Klasse)
class Traffmonetizer(BasicSource):
    var_name = "Cli"
    network_exchange = 0.10 / 1_000_000_000
    payout_rate = 0.96 * 0.95


# RePocket (Simulierte Klasse)
class RePocket(BasicSource):
    var_name = "node"
    network_exchange = 0.10 / 1_000_000_000
    payout_rate = 0.91


# EarnFM (Simulierte Klasse)
class EarnFM(BasicSource):
    var_name = "earnfm_example"
    network_exchange = 0.25 / 1_000_000_000


if __name__ == '__main__':
    EarnFM().get_data_usage_today()
