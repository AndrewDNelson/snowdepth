import argparse

from datetime import datetime

def add_date_arg(parser: argparse.ArgumentParser) -> None:
    parser.add_argument(
        "--date",
        type=str,
        default=datetime.today().strftime("%Y-%m-%d"),
        help="Date (format: YYYY-MM-DD). Defaults to today."
    )