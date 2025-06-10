"""Convert SNODAS binary file to GeoTIFF."""

import subprocess

from datetime import datetime
from pathlib import Path

from ingest.common import build_output_dir, parse_args

# ========== Configuration ==========

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
    output_dir = build_output_dir(date, BASE_DIR)

    file_name = next((f for f in output_dir.iterdir() if f.suffix == ".dat"), None)
    if not file_name:
        raise RuntimeError(f"No .dat file found in {output_dir}")
    
    dat_path = file_name.with_suffix(".dat")
    tif_path = file_name.with_suffix(".tif")
    hdr_path = file_name.with_suffix(".hdr")
    
    with open(hdr_path, "x") as f:
        f.write(HDR_CONTENT)

    gdal_translate(dat_path, tif_path)

def gdal_translate(input_path: Path, output_path: Path) -> None:
    """Run gdal translate command."""
    subprocess.run(
        ["gdal_translate", "-of", "GTiff", "-a_srs", "+proj=longlat +ellps=WGS84 +datum=WGS84 +no_defs", "-a_nodata", "-9999", "-a_ullr", "-130.51708333333333", "58.23291666666667", "-62.25041666666667", "24.09958333333333", str(input_path), str(output_path)]
        check=True,
        capture_output=True
        text=True
    )

def main() -> None:
    args = parse_args()
    target_date = datetime.strptime(args.date, "%Y-%m-%d") if args.date else datetime.today()
    convert_snodas(target_date)

if __name__ == "__main__":
    main()
