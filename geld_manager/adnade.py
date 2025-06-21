from pathlib import Path
from time import time
from basic_source import BasicSource, Status
from os import environ


class Adnade(BasicSource):
    currency = "€"

    def get_status(self) -> Status:
        """Get the status of the source."""
        status_file = self.base_path / "adnade" / "status"
        if not status_file.exists():
            return Status.ERROR

        status = int(status_file.read_text())
        if status > time():
            return Status.OK
        else:
            return Status.ERROR

    def get_balance(self) -> float:
        """Get the total balance of the account."""
        points = 0
        for file in (self.base_path / "adnade").rglob("*"):
            if file.name == "status":
                continue
            points += int(file.read_text())

        return points / 4 * 0.9 / 100_000 * 4.2

    def get_balance_today(self) -> float:
        """Get the balance earned today."""
        return 0

    def get_data_usage(self) -> int:
        """Get the total data usage statistics."""
        return 0

    def get_data_usage_today(self) -> int:
        """Get the data usage statistics for today."""
        return 0
