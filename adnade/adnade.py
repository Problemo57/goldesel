from os import environ
from pathlib import Path
from random import randbytes, random, choices, randint
from re import search
from time import sleep, time
from hashlib import sha1
from datetime import datetime
from uuid import uuid4
from concurrent.futures import ThreadPoolExecutor

from requests import Session, post

user_agent = environ.get('USERAGENT', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:128.0) Gecko/20100101 Firefox/128.0')
username = environ.get('USERNAME', 'problemo')
device_name = environ.get('DEVICE_NAME', '')


class AdnadeSurfbar:
    points_per_refresh = 0.4
    base_dir = Path("/var/lib/goldesel/adnade")

    def __init__(self, surfbar_name: str, device_name: str = ""):
        self.count = 2  # changing param to prevent IE caching.
        self.refresh_count = 0
        self.points_file_uuid = str(uuid4())
        self.surfbar_id = None

        self.username = surfbar_name
        self.device_name = device_name
        self.session = Session()
        self.session.headers.update({
            'User-Agent': user_agent,
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'de,en-US;q=0.7,en;q=0.3',
        })

        self.bettel_credits = 0.0
        self.bettel_tsp = None
        self.bettel_a = None
        self.bettel_session = Session()
        self.bettel_session.headers.update({
            'User-Agent': user_agent,
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'de,en-US;q=0.7,en;q=0.3',
        })

        self.surfbar_ok = False
        self.bettel_ok = False

    def get(self, url, retries: int = 3, **kwargs):
        try:
            return self.session.get(url, **kwargs)

        except Exception as e:
            if retries <= 0:
                raise e
            sleep(10)
            return self.get(url, retries - 1, **kwargs)

    def bettel_get(self, url, retries: int = 3, **kwargs):
        try:
            return self.bettel_session.get(url, **kwargs)

        except Exception as e:
            if retries <= 0:
                raise e
            sleep(10)
            return self.bettel_get(url, retries - 1, **kwargs)

    def save_points_data(self):
        points_file = self.base_dir / datetime.now().date().isoformat() / self.points_file_uuid
        points_file.parent.mkdir(parents=True, exist_ok=True)
        points_file.write_text(str(self.bettel_credits))

    def save_state(self):
        points_file = self.base_dir / "status"
        points_file.parent.mkdir(parents=True, exist_ok=True)
        points_file.write_text(str(self.surfbar_ok and self.bettel_ok))

    def get_matomo_cookies(self) -> dict[str, str]:
        url = "adnade.net/"
        site_id = "43o5DrNpGEM1"

        host_hash = sha1(url.encode()).hexdigest()[:4]
        timestamp = time().__floor__()
        uuid = randbytes(8).hex()

        pv_id = ''.join(choices("abcdefghijklmnopqrstuvwxyz0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ", k=6))

        today = datetime.now()
        params = {
            'action_name': 'AdNade.net - Surfbar',
            'idsite': site_id,
            'rec': '1',
            'r': str(random())[2:8],
            'h': today.hour,
            'm': today.minute,
            's': today.second,
            'url': f'https://adnade.net/surfbar_oben.php?surfsid={self.surfbar_id}',
            'urlref': f'https://adnade.net/view.php?surfsid={self.surfbar_id}',
            '_id': uuid,
            '_idn': '1',
            'send_image': '0',
            '_refts': '0',
            'pdf': '1',
            'qt': '0',
            'realp': '0',
            'wma': '0',
            'fla': '0',
            'java': '0',
            'ag': '0',
            'cookie': '1',
            'res': '1920x1080',
            'pv_id': pv_id,
            'pf_net': '0',
            'pf_srv': randint(20, 25),
            'pf_tfr': randint(0, 1),
            'pf_dm1': randint(200, 300),
            'uadata': '{}',
        }
        headers = {
            'User-Agent': user_agent,
            'Accept': '*/*',
            'Accept-Language': 'de,en-US;q=0.7,en;q=0.3',
            'Content-Type': 'application/x-www-form-urlencoded; charset=utf-8',
            'Origin': 'null',
            'Sec-GPC': '1',
            'Connection': 'keep-alive',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'no-cors',
            'Sec-Fetch-Site': 'cross-site',
            'Priority': 'u=6',
        }

        post('https://tool.hubu.link/matomo.php', params=params, headers=headers)

        return {
            f"_pk_id.{site_id}.{host_hash}": f"{uuid}.{timestamp}.",
            f"_pk_ses.{site_id}.{host_hash}": "1"
        }

    def get_surfbar_id(self) -> str:
        response = self.get(f"https://adnade.net/view.php?user={self.username}&multi=4")
        if not response.history:
            print("Error on init_surfbar, no history!")
            self.surfbar_ok = False
            raise RuntimeError("Error on init_surfbar, no history!")

        self.surfbar_id = response.url.split("surfsid=")[1].split("&")[0]
        return self.surfbar_id

    def init_surfbar(self):
        self.get_surfbar_id()

        params = {
            'surfsid': self.surfbar_id,
        }

        self.get('https://adnade.net/surfbar_oben.php', params=params)

        for i in range(1, 5):
            params = {
                'nr': i,
                'surfsid': self.surfbar_id,
            }
            self.get('https://adnade.net/surfbar_multi_frame.php', params=params)

        for i in range(1, 5):
            params = {
                'nr': i,
                'surfsid': self.surfbar_id,
            }
            self.get('https://adnade.net/surfbar_multi_oben.php', params=params)

        self.refresh_multi_surfbar()

        matomo_cookies = self.get_matomo_cookies()
        self.session.cookies.update(matomo_cookies)

    def refresh_surfbar(self, nr: int = 1):
        self.count += 1
        self.refresh_count += 1

        params = {
            'nr': nr,
            'surfsid': self.surfbar_id,
            'cnt': self.count,
        }
        response = self.get('https://adnade.net/surfbar_mitte.php', params=params)
        if 'Achtung!' in response.text:
            print("Error on refresh_surfbar, Surfbar got timeout.")
            self.surfbar_ok = False
            raise RuntimeError("Error on refresh_surfbar, Surfbar got timeout.")

    def refresh_multi_surfbar(self):
        for i in range(1, 5):
            self.refresh_surfbar(i)

    def run_surfbar(self):
        surfbar_id = str(uuid4())
        while True:
            try:
                if not self.surfbar_id or self.count >= 2000:
                    self.init_surfbar()

                self.refresh_multi_surfbar()
                print(f"Refreshed Surfbar: {self.count} times.")
                Path("health.txt").write_text(f"{int(time()) + 200}")
                Path("/var/lib/goldesel/adnade").mkdir(parents=True, exist_ok=True)
                Path(f"/var/lib/goldesel/adnade/status").write_text(f"{int(time()) + 200}")
                Path(f"/var/lib/goldesel/adnade/{surfbar_id}").write_text(f"{self.count}")
                self.surfbar_ok = True
                sleep(122)

            except Exception as e:
                print(f"Error on run_surfbar: {e}")
                surfbar_id = str(uuid4())
                self.surfbar_ok = False
                sleep(60)

    def init_bettel_link(self):
        params = {
            'user': self.username,
            'subid': self.device_name,
        }

        response = self.bettel_get('https://adnade.net/ptp/', params=params)
        update_url_match = search(r'index\.php\?tsp=([^&]*)&a=([^&]*)&', response.text)
        if update_url_match is None:
            print("Error on init_bettel_link, no update url found!")
            self.bettel_ok = False
            raise RuntimeError("Error on init_bettel_link, no update url found!")

        self.bettel_tsp = update_url_match.group(1)
        self.bettel_a = update_url_match.group(2)

        # deliver_url_match = search(r"<iframe src='[^']*id=([^&]*)&d=([^']*)'", response.text)
        # deliver_d = deliver_url_match.group(2)
        #
        # params = {
        #     'id': self.bettel_tsp,
        #     'd': deliver_d,
        # }
        # response = self.bettel_get('https://deliver.adnade.net/', params=params)
        # surfid_match = search(r'klick4creditsgoto\.php\?surfsid=([^\"]*)', response.text)

        params = {
            'surfsid': self.get_surfbar_id(),
        }
        response2 = self.bettel_get('https://adnade.net/klick4creditsgoto.php', params=params)

        pass

        matomo_cookies = self.get_matomo_cookies()
        self.bettel_session.cookies.update(matomo_cookies)

    def refresh_bettel_link(self):
        if self.bettel_tsp is None:
            self.init_bettel_link()

        params = {
            'tsp': self.bettel_tsp,
            'a': self.bettel_a,
            'd': (time() * 1000).__floor__(),
        }

        response = self.bettel_get('https://adnade.net/ptp/index.php', params=params)
        self.bettel_credits = float(response.text)

    def run_bettel_link(self):
        while True:
            try:
                self.refresh_bettel_link()
                print(f"Earned Bettel Credits: {self.bettel_credits}")
                self.bettel_ok = True
                sleep(10)

            except Exception as e:
                print(f"Error on run_bettel_link: {e}")
                self.bettel_ok = False
                sleep(60)

    def update_status(self):
        while True:
            self.save_state()
            self.save_points_data()
            sleep(10)


def main():
    # while True:
    #     try:
    #         with ThreadPoolExecutor() as executor:
    #             adnade = AdnadeSurfbar(username, device_name)
    #             executor.submit(adnade.run_bettel_link)
    #             executor.submit(adnade.run_surfbar)
    #             executor.submit(adnade.update_status)
    #             executor.shutdown(wait=True)
    #
    #     except Exception as e:
    #         print(f"Error on run_surfbar: {e}")
    #         sleep(60)
    while True:
        try:
            AdnadeSurfbar(username).run_surfbar()

        except Exception as e:
            print(f"Error on run_surfbar: {e}")
            sleep(60)


if __name__ == '__main__':
    main()
