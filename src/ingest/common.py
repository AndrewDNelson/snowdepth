from datetime import datetime
from pathlib import Path

def format_date(date: datetime) -> str:
    return date.strftime("%Y"), date.strftime("%m"), date.strftime("%d"), date.strftime("%m_%b"), date.strftime("%Y%m%d")

def build_output_dir(date: datetime, base_dir: Path):
    year, month, day = format_date(date)[:3]
    return base_dir / year / month / day
