import os
import requests
import tarfile
from datetime import datetime
from pathlib import Path

# ========== Configuration ==========

BASE_DIR = "data"
BASE_URL = "https://noaadata.apps.nsidc.org/NOAA/G02158/unmasked"
DEFAULT_DATE = datetime.today()

# ========== Functions ==========

def build_snodas_url(date: datetime) -> str:
    year = date.strftime("%Y")
    month_str = date.strftime("%m_%b")  # e.g., "05_May"
    file_date_str = date.strftime("%Y%m%d")
    filename = f"SNODAS_unmasked_{file_date_str}.tar"
    return f"{BASE_URL}/{year}/{month_str}/{filename}", filename

def build_output_path(date: datetime) -> str:
    """
    Constructs the output path for the downloaded file based on the date.
    """
    year = date.strftime("%Y")
    month_str = date.strftime("%m_%b")  # e.g., "05_May"
    file_date_str = date.strftime("%Y%m%d")
    filename = f"SNODAS_unmasked_{file_date_str}.tar"
    return os.path.join(BASE_DIR, year, month_str)


def download_snodas_file(date: datetime):
    """
    Downloads the SNODAS .tar file for a given date and saves it to OUTPUT_DIR.
    """
    url, filename = build_snodas_url(date)
    local_path = build_output_path(date)
    output_dir = os.path.join(local_path, filename)

    print(f"url: {url}")
    print(f"filename: {filename}")
    print(f"local path: {local_path}")

    print(f"Downloading SNODAS file for {date.strftime('%Y-%m-%d')}...")
    print(f"URL: {url}")

    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()

        os.makedirs(local_path, exist_ok=True)

        with open(output_dir, "wb") as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)

        print(f"Saved to {output_dir}")

        with tarfile.open(output_dir, "r") as tar:
            tar.extractall(path=local_path)
        print(f"Extracted {filename} to {local_path}")

        os.remove(output_dir)
        print(f"Removed tar file {output_dir}")



    except requests.exceptions.RequestException as e:
        print(f"Download failed: {e}")

# ========== Main ==========

if __name__ == "__main__":
    target_date = DEFAULT_DATE.replace(year=2025, month=5, day=12)
    download_snodas_file(target_date)
