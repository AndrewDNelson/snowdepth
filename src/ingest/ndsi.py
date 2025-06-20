"""Download NDSI HDF files from NASA's EarthData."""

import logging
import os
import re

from datetime import datetime
from pathlib import Path
from typing import List

import requests
import bs4

from common.cli import CustomArgumentParser
from common.logging_utils import setup_logging
from ingest.common import build_output_dir, format_date

# ========== Configuration ==========

logger = logging.getLogger(__name__)
BASE_DIR = Path("data/ndsi")
BASE_URL = "https://cmr.earthdata.nasa.gov/virtual-directory/collections/C3028765772-NSIDC_CPRD/temporal"

def setup_netrc() -> None:
    """Retrieve environment variable for authentication."""
    netrc_path = Path.home() / ".netrc"
    if not netrc_path.exists():
        USERNAME = os.getenv("EARTHDATA_USERNAME")
        PASSWORD = os.getenv("EARTHDATA_PASSWORD")
        if not USERNAME or not PASSWORD:
            logger.error("Missing EARTHDATA_USERNAME or EARTHDATA_PASSWORD in environment.")
            raise RuntimeError("Missing EARTHDATA_USERNAME or EARTHDATA_PASSWORD")

        netrc_path.write_text(
            f"machine urs.earthdata.nasa.gov\nlogin {USERNAME}\npassword {PASSWORD}\n"
        )
        os.chmod(netrc_path, 0o600)

# ========== Utility Functions ==========

def build_nasa_url(date: datetime) -> str:
    """Return the listing URL for *date*."""
    year, month, day = format_date(date)[:3]
    return f"{BASE_URL}/{year}/{month}/{day}/"

def fetch_hdf_links(url: str) -> List[str]:
    """Return HDF file URLs found at the given *url*."""
    try:
        page = requests.get(url)
        page.raise_for_status()
    except requests.RequestException as exc:
        logger.error("Failed to fetch listing from %s: %s", url, exc)
        return[]
    
    soup = bs4.BeautifulSoup(page.text, "html.parser")

    # Find all .hdf file links
    links = soup.find_all('a', href=re.compile(r'\.hdf$'))
    hrefs = [link['href'] for link in links if link.has_attr('href')]
    return [href if href.startswith("http") else url + href for href in hrefs]

def download_ndsi_files(date: datetime) -> None:
    """Download all HDF files for *date* into the configured directory."""
    url = build_nasa_url(date)
    hrefs = fetch_hdf_links(url)

    if not hrefs:
        logger.warning("No .hdf download links found at %s", url)
        return
    
    output_dir = build_output_dir(date, BASE_DIR / "raw")
    os.makedirs(output_dir, exist_ok=True)

    success_count = 0
    with requests.Session() as session:
        for href in hrefs:
            local_filename = href.split("/")[-1]
            local_path = output_dir / local_filename

            try:
                response = session.get(href, allow_redirects=False)

                if response.status_code in (302, 303):
                    signed_url = response.headers["Location"]

                    with session.get(signed_url, stream=True) as r:
                        r.raise_for_status()
                        with open(local_path, "wb") as f:
                            for chunk in r.iter_content(chunk_size=8192):
                                f.write(chunk)

                    success_count += 1
                    logger.info("Saved %s", local_path)
                else:
                    logger.error(
                        "Unexpected response code %s for %s", 
                        response.status_code, 
                        href,
                    )
                    
            except requests.exceptions.RequestException as exc:
                logger.error("Download failed for %s: %s", href, str(exc))
        logger.info("Successfully downloaded %s of %s NDSI files.", success_count, len(hrefs))

def run(date: datetime) -> None:
    setup_netrc()
    download_ndsi_files(date)

def main() -> None:
    parser = CustomArgumentParser()
    parser.add_date_arg()
    args = parser.parse_args()
    target_date = datetime.strptime(args.date, "%Y-%m-%d") if args.date else datetime.today()
    setup_logging()
    run(target_date)

if __name__ == "__main__":
    main()