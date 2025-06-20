from datetime import datetime

from common.logging_utils import setup_logging
from ingest.ndsi import run as ingest_ndsi

def parse_args():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--date",
        type=str,
        default=datetime.today().strftime("%Y-%m-%d"),
        help="Date (format: YYYY-MM-DD). Defaults to today."
    )
    return parser.parse_args()

def main():
    args = parse_args()
    date = datetime.strptime(args.date, "%Y-%m-%d") if args.date else datetime.today()

    setup_logging()
    ingest_ndsi(date)
    # call modules here?
    # run snodas ingest
    # run snodas process
    # run ndsi ingest
    # run ndsi process


if __name__ == "__main__":
    main()
