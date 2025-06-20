"""Convert SNODAS binary file to GeoTIFF."""

import logging
import os
import subprocess

from datetime import datetime
from pathlib import Path

from common.cli import CustomArgumentParser
from common.logging_utils import setup_logging
from ingest.common import build_output_dir

# ========== Configuration ==========

logger = logging.getLogger()
BASE_DIR = Path("data/snodas")
HDR_CONTENT = """ENVI
samples = 8192
lines = 4096
bands = 1
header offset = 0
file type = ENVI Standard
data type = 2
interleave = bsq
byte order = 1"""

def convert_snodas(date: datetime) -> None:
    """Generate header file in data directory, then create GeoTIFF"""
    raw_dir = build_output_dir(date, BASE_DIR / "raw")
    converted_dir = build_output_dir(date, BASE_DIR / "converted")

    file_path = next((f for f in raw_dir.iterdir() if f.suffix == ".dat"), None)
    if not file_path:
        raise RuntimeError(f"No .dat file found in {raw_dir}")
    
    dat_path = file_path.with_suffix(".dat")
    hdr_path = file_path.with_suffix(".hdr")
    with open(hdr_path, "x") as f:
        f.write(HDR_CONTENT)

    tif_path = converted_dir / file_path.with_suffix(".tif").name
    os.makedirs(converted_dir, exist_ok=True)
    dat_to_tif(dat_path, tif_path)

def dat_to_tif(input_path: Path, output_path: Path) -> None:
    """Run gdal translate command."""
    subprocess.run(
        ["gdal_translate", "-of", "GTiff", "-a_srs", "+proj=longlat +ellps=WGS84 +datum=WGS84 +no_defs", "-a_nodata", "-9999", "-a_ullr", "-130.51708333333333", "58.23291666666667", "-62.25041666666667", "24.09958333333333", str(input_path), str(output_path)],
        check=True,
        capture_output=True,
        text=True
    )

def run(date: datetime) -> None:
    convert_snodas(date)

def main() -> None:
    parser = CustomArgumentParser()
    parser.add_date_arg()
    args = parser.parse_args()
    target_date = datetime.strptime(args.date, "%Y-%m-%d") if args.date else datetime.today()
    setup_logging()
    run(target_date)

if __name__ == "__main__":
    main()
