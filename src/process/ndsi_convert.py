"""Convert ndsi hdf file to GeoTIFF."""

import argparse
import os
import subprocess

from datetime import datetime
from pathlib import Path

from ingest.common import build_output_dir
from common.cli import add_date_arg

# ========== Configuration ==========

BASE_DIR = Path("data/ndsi")

def hdf_to_tif(input_path: Path, output_path: Path):
    try:
        subprocess.run(
            ["gdal_translate", f"HDF4_EOS:EOS_GRID:{input_path}:MOD_Grid_Snow_500m:MOD10A1_NDSI_Snow_Cover", str(output_path)],
            check=True, 
            capture_output=True, 
            text=True
        )
    except subprocess.CalledProcessError as e:
        print("gdal_translate failed")
        print(e.stderr)
        raise

def convert_ndsi(date: datetime) -> None:
    """Generate header file in data directory, then create GeoTIFF"""
    raw_dir = build_output_dir(date, BASE_DIR / "raw")
    converted_dir = build_output_dir(date, BASE_DIR / "converted")

    files = list(f for f in raw_dir.iterdir() if f.suffix == ".hdf")
    if not files:
        raise RuntimeError(f"No .hdf files found in {raw_dir}")
    
    for hdf_path in files:
        tif_path = converted_dir / hdf_path.with_suffix(".tif").name
        os.makedirs(converted_dir, exist_ok=True)
        hdf_to_tif(hdf_path, tif_path)

def run(date: datetime) -> None:
    convert_ndsi(date)

def main() -> None:
    parser = argparse.ArgumentParser()
    add_date_arg(parser)
    args = parser.parse_args()
    target_date = datetime.strptime(args.date, "%Y-%m-%d") if args.date else datetime.today()
    run(target_date)

if __name__ == "__main__":
    main()
