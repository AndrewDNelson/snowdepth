"""Convert ndsi hdf file to GeoTIFF."""

import logging
import os
import subprocess

from datetime import datetime
from pathlib import Path

from ingest.common import build_output_dir
from common.logging_utils import setup_logging
from common.cli import CustomArgumentParser

# ========== Configuration ==========

logger = logging.getLogger(__name__)
BASE_DIR = Path("data/ndsi")

def hdf_to_tif(input_path: Path, output_path: Path):
    try:
        subprocess.run(
            ["gdal_translate", f"HDF4_EOS:EOS_GRID:{input_path}:MOD_Grid_Snow_500m:MOD10A1_NDSI_Snow_Cover", str(output_path)],
            check=True, 
            capture_output=True, 
            text=True
        )
        logger.info("Converted %s to %s.", input_path.name, output_path.name)
    except subprocess.CalledProcessError as e:
        logger.error("gdal_translate failed for %s: %s", input_path.name, e.stderr)
        raise

def convert_ndsi(date: datetime) -> None:
    """Generate header file in data directory, then create GeoTIFF"""
    raw_dir = build_output_dir(date, BASE_DIR / "raw")
    converted_dir = build_output_dir(date, BASE_DIR / "converted")

    files = list(raw_dir.glob('*.hdf'))
    if not files:
        logger.error(f"NSDI conversion failed. No .hdf files found in {raw_dir}")
        raise FileNotFoundError(f"No .hdf files found in {raw_dir}")
    
    os.makedirs(converted_dir, exist_ok=True)
    for hdf_path in files:
        tif_path = converted_dir / hdf_path.with_suffix(".tif").name
        logger.info("Starting conversion of %s to %s.", hdf_path.name, tif_path.name)
        hdf_to_tif(hdf_path, tif_path)

def run(date: datetime) -> None:
    convert_ndsi(date)

def main() -> None:
    parser = CustomArgumentParser()
    parser.add_date_arg()
    args = parser.parse_args()
    target_date = datetime.strptime(args.date, "%Y-%m-%d") if args.date else datetime.today()
    setup_logging()
    run(target_date)

if __name__ == "__main__":
    main()
