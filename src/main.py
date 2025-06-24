from datetime import datetime

from common.logging_utils import setup_logging
from common.cli import CustomArgumentParser

from ingest.ndsi import run as ingest_ndsi
from ingest.snodas import run as ingest_snodas
from process.ndsi_convert import run as convert_ndsi
from process.snodas_convert import run as convert_snodas

def main():
    parser = CustomArgumentParser()
    parser.add_date_arg()
    args = parser.parse_args()
    date = datetime.strptime(args.date, "%Y-%m-%d") if args.date else datetime.today()

    setup_logging()
    # ingest_ndsi(date)
    # ingest_snodas(date)
    # convert_ndsi(date)
    # convert_snodas(date)

    # argparse: custom inheritance maybe? CustomArgumentParser?
    # use new structured logs (get rid of setup_logging from src/ingest/common.py)
    # add useful logs

if __name__ == "__main__":
    main()
