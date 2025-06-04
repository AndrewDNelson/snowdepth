import logging
from datetime import datetime
from pathlib import Path

def setup_logging(name: str, date: str):
    logs_dir = Path("logs")
    logs_dir.mkdir(exist_ok=True)

    log_path = f"logs/{name}_{date}.log"

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(message)s",
        handlers=[
            logging.FileHandler(log_path),
            logging.StreamHandler() # also logs to console
        ]
    )

def format_date(date: datetime) -> str:
    return date.strftime("%Y"), date.strftime("%m"), date.strftime("%d"), date.strftime("%m_%b"), date.strftime("%Y%m%d")

def build_output_dir(date: datetime, base_dir: Path):
    year, month, day = format_date(date)[:3]
    return base_dir / year / month / day