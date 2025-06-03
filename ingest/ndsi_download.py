import argparse
import os
import requests
import bs4
import re
from pathlib import Path
from datetime import datetime

# ========== Configuration ==========

parser = argparse.ArgumentParser()
parser.add_argument("--date", type=str, help="Target date (YYYY-MM-DD)")
args = parser.parse_args()

BASE_DIR = Path("data/ndsi")
BASE_URL = "https://cmr.earthdata.nasa.gov/virtual-directory/collections/C3028765772-NSIDC_CPRD/temporal"
DEFAULT_DATE = datetime.strptime(args.date, "%Y-%m-%d") if args.date else datetime.today()

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

target_date = DEFAULT_DATE.replace(year=2025, month=5, day=17)
url = build_nasa_url(target_date)

page = requests.get(url)
html = page.content.decode("utf-8", errors="replace")
data = bs4.BeautifulSoup(html, "html.parser")

# Find all .hdf file links
links = data.find_all('a', href=re.compile(r'\.hdf$'))
hrefs = [link['href'] for link in links if link.has_attr('href')]

if not hrefs:
    print("No .hdf download links found.")
else:
    output_dir = build_output_dir(target_date)
    os.makedirs(output_dir, exist_ok=True)

    with requests.Session() as session:

        for href in hrefs:
            download_url = href if href.startswith("http") else url + href
            local_filename = download_url.split("/")[-1]
            local_path = output_dir / local_filename

            try:
                print(f"Requesting: {download_url}")
                response = session.get(download_url, allow_redirects=False)

                if response.status_code in (302, 303):
                    signed_url = response.headers["Location"]
                    print("Redirected to signed URL")

                    r = session.get(signed_url, stream=True)
                    r.raise_for_status()

                    with open(local_path, "wb") as f:
                        for chunk in r.iter_content(chunk_size=8192):
                            f.write(chunk)
                    print(f"Saved to {local_path}")
                else:
                    print(f"Unexpected response code {response.status_code} for {download_url}")
                    print(response.text[:500])
                    
            except requests.exceptions.RequestException as e:
                print(f"Failed to download {download_url}: {e}")
                print(f"Status Code: {getattr(response, 'status_code', 'N/A')}")
                if hasattr(response, 'text'):
                    print(response.text[:500])
