import os

from pathlib import Path
from datetime import datetime
from ingest.common import build_output_dir, parse_args

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

def create_header(date: datetime):
    """Generate header file in data directory"""
    output_dir = build_output_dir(date, BASE_DIR)

    file_name = next((f for f in output_dir.iterdir() if f.suffix == ".dat"), None)
    if not file_name:
        raise RuntimeError(f"No .dat file found in {output_dir}")
    
    hdr_path = file_name.with_suffix(".hdr")
    
    with open(hdr_path, "x") as f:
        f.write(HDR_CONTENT)

def convert_snodas(date: datetime):
    """Create GeoTIFF file from .dat"""
    create_header(date)

    """
    3. Run the command: gdal_translate -of GTiff -a_srs '+proj=longlat +ellps=WGS84 +datum=WGS84 +no_defs' -a_nodata -9999 -a_ullr -130.51708333333333 58.23291666666667 -62.25041666666667 24.09958333333333 <input.dat> <output.tif>
    """



def main() -> None:
    args = parse_args()
    target_date = datetime.strptime(args.date, "%Y-%m-%d") if args.date else datetime.today()
    convert_snodas(target_date)

if __name__ == "__main__":
    main()
