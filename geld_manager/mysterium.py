from requests import get
from datetime import datetime

from basic_source import BasicSource, Status


class Mysterium(BasicSource):
    base_url = "http://127.0.0.1:4050"
    currency = "MYST"
    payout_rate = 0.80 * 0.98 * 0.99 * 0.70
    # 20% Mysterium Payout Fee
    # 2% Exchange Fee to POL
    # 1% Network Fee
    # 30% Exchange Fee to Euro

    def get_status(self) -> Status:
        try:
            response = get(f"{self.base_url}/node/provider/activity-stats")
            online_percent = response.json()['online_percent']
            if online_percent >= 90:
                return Status.OK

            else:
                print(f"Online percent: {online_percent}")
                return Status.UNKNOWN

        except Exception as e:
            print(f"Error on get_status: {e}")
            return Status.ERROR

    def get_balance(self) -> float:
        response = get(f"{self.base_url}/sessions/stats-aggregated").json()['stats']
        return response['sum_tokens'] / 1_000_000_000_000_000_000  # convert wei to normal token.

    def get_balance_today(self) -> float:
        params = {
            "date_from": datetime.now().date().isoformat()
        }
        response = get(f"{self.base_url}/sessions/stats-aggregated", params=params).json()['stats']
        return response['sum_tokens'] / 1_000_000_000_000_000_000  # convert wei to normal token.

    def get_data_usage(self) -> int:
        response = get(f"{self.base_url}/sessions/stats-aggregated").json()['stats']
        return max(response['sum_bytes_received'], response['sum_bytes_sent'])

    def get_data_usage_today(self) -> int:
        params = {
            "date_from": datetime.now().date().isoformat()
        }

        response = get(f"{self.base_url}/sessions/stats-aggregated", params=params).json()['stats']
        return max(response['sum_bytes_received'], response['sum_bytes_sent'])


if __name__ == '__main__':
    m = Mysterium()
    print(m.get_balance())
