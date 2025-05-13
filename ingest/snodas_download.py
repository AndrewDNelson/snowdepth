import os
import requests
from datetime import datetime
from pathlib import Path

# ========== Configuration ==========

OUTPUT_DIR = "data"
BASE_URL = "https://noaadata.apps.nsidc.org/NOAA/G02158/unmasked"
DEFAULT_DATE = datetime.today()

# ========== Functions ==========

def build_snodas_url(date: datetime) -> str:
    year = date.strftime("%Y")
    month_str = date.strftime("%m_%b")  # e.g., "05_May"
    file_date_str = date.strftime("%Y%m%d")
    filename = f"SNODAS_unmasked_{file_date_str}.tar"
    return f"{BASE_URL}/{year}/{month_str}/{filename}", filename

def download_snodas_file(date: datetime):
    """
    Downloads the SNODAS .tar file for a given date and saves it to OUTPUT_DIR.
    """
    url, filename = build_snodas_url(date)
    local_path = Path(OUTPUT_DIR) / filename

    print(f"Downloading SNODAS file for {date.strftime('%Y-%m-%d')}...")
    print(f"URL: {url}")

    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()

        os.makedirs(OUTPUT_DIR, exist_ok=True)

        with open(local_path, "wb") as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)

        print(f"Saved to {local_path}")

    except requests.exceptions.RequestException as e:
        print(f"Download failed: {e}")

# ========== Main ==========

if __name__ == "__main__":
    target_date = DEFAULT_DATE.replace(year=2025, month=5, day=12)
    download_snodas_file(target_date)
