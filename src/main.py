from datetime import datetime

from common.logging_utils import setup_logging
from ingest.ndsi import run as ingest_ndsi
from ingest.snodas import run as ingest_snodas
from process.ndsi_convert import run as convert_ndsi
from process.snodas_convert import run as convert_snodas

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
    # ingest_ndsi(date)
    # ingest_snodas(date)
    # convert_ndsi(date)
    # convert_snodas(date)

if __name__ == "__main__":
    main()
