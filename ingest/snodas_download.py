import argparse
import os
import requests
import tarfile
import gzip
import logging
from datetime import datetime
from pathlib import Path

# ========== Configuration ==========

parser = argparse.ArgumentParser()
parser.add_argument("--date", type=str, help="Target date (YYYY-MM-DD)")
args = parser.parse_args()
TARGET_DATE = datetime.strptime(args.date, "%Y-%m-%d") if args.date else datetime.today()
BASE_DIR = Path("data/snodas")
BASE_URL = "https://noaadata.apps.nsidc.org/NOAA/G02158/unmasked"

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

setup_logging("snodas", args.date)

# ========== Utility Functions ==========

def format_date(date: datetime):
    return date.strftime("%Y"), date.strftime("%m_%b"), date.strftime("%Y%m%d"), date.strftime("%d")

def build_snodas_url(date: datetime):
    """
    Builds the SNODAS tar file URL and expected filename for the given date.
    """
    year, month, file_date, _ = format_date(date)
    filename = f"SNODAS_unmasked_{file_date}.tar"
    url = f"{BASE_URL}/{year}/{month}/{filename}"
    return url, filename

def build_output_dir(date: datetime) -> Path:
    """
    Builds the local directory path based on date.
    """
    year, month, _, day = format_date(date)
    return BASE_DIR / year / month / day

# ========== Main Download Logic ==========

def download_snodas_file(date: datetime):
    url, filename = build_snodas_url(date)
    output_dir = build_output_dir(date)
    local_tar_path = output_dir / filename

    logging.info("Starting SNODAS ingest for %s", date.strftime('%Y-%m-%d'))
    logging.info("Downloading from %s", url)

    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()

        os.makedirs(output_dir, exist_ok=True)

        with open(local_tar_path, "wb") as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)

        logging.info("Downloaded %s (%d bytes)", filename, os.path.getsize(local_tar_path))

        # Define which files to keep
        keep_keywords = ["11034"]  # Snow depth only

        # Extract and filter
        with tarfile.open(local_tar_path, "r") as tar:
            members = [m for m in tar.getmembers() if any(k in m.name for k in keep_keywords)]
            tar.extractall(path=output_dir, members=members)

        logging.info("Extracted %s files matching keywords %s", len(members), keep_keywords)
        logging.info("Extracted %d files: %s", len(members), [m.name for m in members][:5])

        os.remove(local_tar_path)
        logging.info("Cleaned up tar file")

        # Extract all .gz files in the output directory
        for gz_file in output_dir.glob("*.gz"):
            extracted_file_path = gz_file.with_suffix('')  # Remove .gz extension
            with gzip.open(gz_file, "rb") as gz:
                with open(extracted_file_path, "wb") as extracted_file:
                    extracted_file.write(gz.read())
            os.remove(gz_file)

    except requests.exceptions.RequestException as e:
        logging.error("Failed to download SNODAS for %s: %s", date, str(e))


# ========== Entry Point ==========

if __name__ == "__main__":
    download_snodas_file(TARGET_DATE)
