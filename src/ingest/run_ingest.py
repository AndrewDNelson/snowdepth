import subprocess
import sys
from datetime import datetime

# ========== Argument Parsing ==========

def parse_args():
    import argparse
    parser = argparse.ArgumentParser(description="Run SNODAS + NDSI ingestion scripts")
    parser.add_argument(
        "--date",
        type=str,
        default=datetime.today().strftime("%Y-%m-%d"),
        help="Date to ingest (format: YYYY-MM-DD). Defaults to today."
    )
    return parser.parse_args()

args = parse_args()
ingest_date = args.date

# ========== Run Ingestion Scripts ==========

print(f"▶ Running SNODAS ingestion for {ingest_date}...")
subprocess.run(
    ["python", "src/ingest/snodas_download.py", "--date", ingest_date],
    check=True
)

print(f"▶ Running NDSI ingestion for {ingest_date}...")
subprocess.run(
    ["python", "src/ingest/ndsi_download.py", "--date", ingest_date],
    check=True
)

print("✅ Ingestion complete.")
