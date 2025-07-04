"""Download SNODAS snow depth files from noaa."""

import gzip
import logging
import os
import tarfile

from datetime import datetime
from pathlib import Path
from typing import Tuple

import requests

from common.cli import CustomArgumentParser
from common.logging_utils import setup_logging
from ingest.common import build_output_dir, format_date

# ========== Configuration ==========

logger = logging.getLogger(__name__)
BASE_DIR = Path("data/snodas")
BASE_URL = "https://noaadata.apps.nsidc.org/NOAA/G02158/unmasked"

# ========== Utility Functions ==========

def build_snodas_url(date: datetime) -> Tuple[str, str]:
    """Builds the SNODAS tar file URL and expected filename for the given date."""
    year, _, _, month_str, file_date = format_date(date)
    filename = f"SNODAS_unmasked_{file_date}.tar"
    url = f"{BASE_URL}/{year}/{month_str}/{filename}"
    return url, filename

# ========== Main Download Logic ==========

def download_snodas_file(date: datetime):
    """Download TAR file for *date* into the configured directory, then it extracts it."""
    url, filename = build_snodas_url(date)
    output_dir = build_output_dir(date, BASE_DIR / "raw")
    local_tar_path = output_dir / filename

    logger.info("Starting SNODAS ingest for %s", date.strftime('%Y-%m-%d'))
    logger.info("Downloading from %s", url)

    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()

        os.makedirs(output_dir, exist_ok=True)

        with open(local_tar_path, "wb") as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)

        logger.info("Downloaded %s (%d bytes)", filename, os.path.getsize(local_tar_path))

        # Define which files to keep
        keep_keywords = ["11034"]  # Snow depth only

        # Extract and filter
        with tarfile.open(local_tar_path, "r") as tar:
            members = [m for m in tar.getmembers() if any(k in m.name for k in keep_keywords)]
            tar.extractall(path=output_dir, members=members)

        logger.info("Extracted %s files matching keywords %s", len(members), keep_keywords)
        logger.info("Extracted %d files: %s", len(members), [m.name for m in members][:5])

        os.remove(local_tar_path)
        logger.info("Cleaned up tar file")

        # Extract all .gz files in the output directory
        for gz_file in output_dir.glob("*.gz"):
            extracted_file_path = gz_file.with_suffix('')  # Remove .gz extension
            with gzip.open(gz_file, "rb") as gz:
                with open(extracted_file_path, "wb") as extracted_file:
                    extracted_file.write(gz.read())
            os.remove(gz_file)

    except requests.exceptions.RequestException as e:
        logger.error("Failed to download SNODAS for %s: %s", date, str(e))

def run(date: datetime) -> None:
    download_snodas_file(date)

def main() -> None:
    parser = CustomArgumentParser()
    parser.add_date_arg()
    args = parser.parse_args()
    target_date = datetime.strptime(args.date, "%Y-%m-%d") if args.date else datetime.today()
    setup_logging()
    run(target_date)

if __name__ == "__main__":
    main()