import argparse

from datetime import datetime

class CustomArgumentParser(argparse.ArgumentParser):
    def add_date_arg(self) -> "CustomArgumentParser":
        self.add_argument(
            "--date",
            type=str,
            default=datetime.today().strftime("%Y-%m-%d"),
            help="Date (format: YYYY-MM-DD). Defaults to today."
        )
        return self