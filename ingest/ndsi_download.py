import argparse
import bs4
import logging
import os
import requests
import re
from datetime import datetime
from pathlib import Path

# ========== Configuration ==========

parser = argparse.ArgumentParser()
parser.add_argument("--date", type=str, help="Target date (YYYY-MM-DD)")
args = parser.parse_args()

BASE_DIR = Path("data/ndsi")
BASE_URL = "https://cmr.earthdata.nasa.gov/virtual-directory/collections/C3028765772-NSIDC_CPRD/temporal"
TARGET_DATE = datetime.strptime(args.date, "%Y-%m-%d") if args.date else datetime.today()

def setup_netrc():
    netrc_path = Path.home() / ".netrc"
    if not netrc_path.exists():
        USERNAME = os.getenv("EARTHDATA_USERNAME")
        PASSWORD = os.getenv("EARTHDATA_PASSWORD")
        if not USERNAME or not PASSWORD:
            raise RuntimeError("Missing EARTHDATA_USERNAME or EARTHDATA_PASSWORD")

        netrc_path.write_text(
            f"machine urs.earthdata.nasa.gov\nlogin {USERNAME}\npassword {PASSWORD}\n"
        )
        os.chmod(netrc_path, 0o600)

setup_netrc()

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

setup_logging("ndsi", args.date)

# ========== Utility Functions ==========

def format_date(date: datetime) -> str:
    return date.strftime("%Y"), date.strftime("%m"), date.strftime("%d")

def build_nasa_url(date: datetime):
    year, month, day = format_date(date)
    url = f"{BASE_URL}/{year}/{month}/{day}/"
    return url

def build_output_dir(date: datetime):
    year, month, day = format_date(date)
    return BASE_DIR / year / month / day
   
# ========== Main Script ==========

url = build_nasa_url(TARGET_DATE)

page = requests.get(url)
html = page.content.decode("utf-8", errors="replace")
data = bs4.BeautifulSoup(html, "html.parser")

# Find all .hdf file links
links = data.find_all('a', href=re.compile(r'\.hdf$'))
hrefs = [link['href'] for link in links if link.has_attr('href')]

if not hrefs:
    logging.warning("No .hdf download links found at %s", url)
else:
    output_dir = build_output_dir(TARGET_DATE)
    os.makedirs(output_dir, exist_ok=True)

    with requests.Session() as session:
        success_count = 0
        for href in hrefs:
            download_url = href if href.startswith("http") else url + href
            local_filename = download_url.split("/")[-1]
            local_path = output_dir / local_filename

            try:
                response = session.get(download_url, allow_redirects=False)

                if response.status_code in (302, 303):
                    signed_url = response.headers["Location"]

                    r = session.get(signed_url, stream=True)
                    r.raise_for_status()

                    with open(local_path, "wb") as f:
                        for chunk in r.iter_content(chunk_size=8192):
                            f.write(chunk)
                    success_count += 1
                    logging.info("Saved to %s", local_path)
                else:
                    logging.error("Unexpected response code %s for %s", response.status_code, download_url)
                    
            except requests.exceptions.RequestException as e:
                logging.error("Download failed for %s: %s", download_url, str(e))
        logging.info("Successfully downloaded %s of %s NDSI files.", success_count, len(hrefs))
