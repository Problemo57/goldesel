from os import environ
from requests import post, get
from pathlib import Path

from basic_source import BasicSource, Status


def get_my_ip():
    response = get('https://api.ipify.org')
    return response.text


# PacketShare (Simulierte Klasse)
class PacketShare(BasicSource):
    var_name = "Packetshare"
    network_exchange = 0.10 / 1_000_000_000

    def __init__(self):
        self.token = None
        if Path('packetshare_token').exists():
            self.token = Path('packetshare_token').read_text()

    def login(self):
        data = {
            'username': environ['PACKETSHARE_USERNAME'],
            'password': environ['PACKETSHARE_PASSWORD'],
        }
        response = post('https://api.packetshare.io/web/user/login', data=data)
        self.token = response.json()['data']['rsp']['session_id']
        Path('packetshare_token').write_text(self.token)

    def post(self, url: str, params: dict = None, data: dict = None):
        if self.token is None:
            self.login()

        headers = {
            'session': self.token,
        }
        response = post('https://api.packetshare.io/web/device/list', data=data, headers=headers, params=params)
        if 'code' in response.json():
            self.login()
            headers = {
                'session': self.token,
            }
            response = post('https://api.packetshare.io/web/device/list', data=data, headers=headers, params=params)

        return response

    def get_status(self) -> Status:
        data = {
            'page': '1',
            'size': '20',
        }
        response = self.post('https://api.packetshare.io/web/device/list', data=data)
        my_device = [d for d in response.json()['data']['list'] if d['ip'] == get_my_ip()]
        if my_device:
            return Status.OK

        return Status.ERROR
