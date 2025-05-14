import os
import requests
import tarfile
from datetime import datetime
from pathlib import Path

# ========== Configuration ==========

BASE_DIR = Path("data")
BASE_URL = "https://noaadata.apps.nsidc.org/NOAA/G02158/unmasked"
DEFAULT_DATE = datetime.today()

# ========== Utility Functions ==========

def format_date(date: datetime):
    return date.strftime("%Y"), date.strftime("%m_%b"), date.strftime("%Y%m%d")

def build_snodas_url(date: datetime):
    """
    Builds the SNODAS tar file URL and expected filename for the given date.
    """
    year, month_str, file_date = format_date(date)
    filename = f"SNODAS_unmasked_{file_date}.tar"
    url = f"{BASE_URL}/{year}/{month_str}/{filename}"
    return url, filename

def build_output_dir(date: datetime) -> Path:
    """
    Builds the local directory path based on date.
    """
    year, month_str, _ = format_date(date)
    return BASE_DIR / year / month_str

# ========== Main Download Logic ==========

def download_snodas_file(date: datetime):
    url, filename = build_snodas_url(date)
    output_dir = build_output_dir(date)
    local_tar_path = output_dir / filename

    print(f"Downloading SNODAS for {date.strftime('%Y-%m-%d')}")
    print(f"URL: {url}")
    print(f"Saving to: {local_tar_path}")

    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()

        os.makedirs(output_dir, exist_ok=True)

        with open(local_tar_path, "wb") as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)

        print(f"Downloaded to {local_tar_path}")

        with tarfile.open(local_tar_path, "r") as tar:
            tar.extractall(path=output_dir)
        print(f"Extracted contents to {output_dir}")

        os.remove(local_tar_path)
        print(f"Cleaned up tar file")

    except requests.exceptions.RequestException as e:
        print(f"Download failed: {e}")

# ========== Entry Point ==========

if __name__ == "__main__":
    target_date = DEFAULT_DATE.replace(year=2025, month=5, day=12)
    download_snodas_file(target_date)
