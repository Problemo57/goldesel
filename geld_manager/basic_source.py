from enum import Enum
from pathlib import Path
from time import time


def parse_network_data(data: str) -> (int, int):
    lines = data.splitlines()
    eth0 = [line for line in lines if 'eth0' in line][0]
    components = eth0.split()
    return int(components[1]), int(components[9])


class Status(Enum):
    OK = "OK"
    ERROR = "ERROR"
    UNKNOWN = "UNKNOWN"


class BasicSource:
    """Base class for implementing various data sources."""
    base_path = Path("/var/lib/goldesel")
    var_name = None
    network_exchange = None  # as USD/Byte
    currency = "$"
    payout_rate = 1  # % rate of how much Money is actually payout out.
    _last_data_usage = 0
    _last_data_change_time = 0

    def get_status(self) -> Status:
        """Get the status of the source."""
        if self.var_name is None:
            raise Exception("Not implemented")

        source_path = self.base_path / self.var_name
        if not source_path.exists():
            return Status.ERROR

        try:
            # Überprüfe, ob sich get_data_usage_today in den letzten 15 Minuten geändert hat
            current_data_usage = self.get_data_usage_today()
            
            if self._last_data_usage != current_data_usage:
                self._last_data_usage = current_data_usage
                self._last_data_change_time = time()
            elif time() - self._last_data_change_time > 60*15:  # 15 Minuten
                return Status.ERROR
                
            latest_file = max(
                (f for f in source_path.rglob("*") if f.is_file()),
                key=lambda x: x.stat().st_mtime,
                default=None
            )

            if latest_file is None:
                return Status.ERROR

            timestamp = int(latest_file.stat().st_mtime)
            if time() - timestamp > 60*5:
                return Status.ERROR

            return Status.OK

        except Exception as e:
            print(f"Error on get_status: {e}")
            return Status.UNKNOWN
        
    def get_balance(self) -> float:
        """Get the total balance of the account."""
        if self.network_exchange is None:
            raise Exception("Not implemented")
        return self.get_data_usage() * self.network_exchange

    def get_balance_today(self) -> float:
        """Get the balance earned today."""
        if self.network_exchange is None:
            raise Exception("Not implemented")
        return self.get_data_usage_today() * self.network_exchange

    def get_data_usage(self) -> int:
        """Get the total data usage statistics."""
        if self.var_name is None:
            raise Exception("Not implemented")

        source_path = self.base_path / self.var_name
        if not source_path.exists():
            return 0

        total_bytes = 0
        for file in source_path.rglob("*/*"):
            if file.name == "net_total":
                net_recv, net_sent = parse_network_data(file.read_text())
                total_bytes += min(net_recv, net_sent)

        return total_bytes

    def get_data_usage_today(self) -> int:
        """Get the data usage statistics for today."""
        if self.var_name is None:
            raise Exception("Not implemented")

        source_path = self.base_path / self.var_name
        if not source_path.exists():
            return 0

        latest_folder = max(
            (f for f in source_path.iterdir() if f.is_dir() and f.name != "timestamp"),
            key=lambda x: x.stat().st_mtime
        )

        if (latest_folder / "net_today").exists():
            net_recv, net_sent = parse_network_data((latest_folder / "net_today").read_text())
            net_recv_total, net_sent_total = parse_network_data((latest_folder / "net_total").read_text())
            net_recv_total -= net_recv
            net_sent_total -= net_sent

            return min(net_recv_total, net_sent_total)

        return 0
