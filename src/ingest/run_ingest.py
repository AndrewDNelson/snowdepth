import subprocess
import sys
from datetime import datetime

# ========== Argument Parsing ==========

def parse_args():
    import argparse
    parser = argparse.ArgumentParser(description="Run SNODAS + NDSI ingestion scripts")
    parser.add_argument(
        "--date",
        type=str,
        default=datetime.today().strftime("%Y-%m-%d"),
        help="Date to ingest (format: YYYY-MM-DD). Defaults to today."
    )
    return parser.parse_args()

args = parse_args()
ingest_date = args.date

def script(arg):
    try:
        subprocess.run(
            arg,
            check=True,
            capture_output=True,
            text=True
        )
    except subprocess.CalledProcessError as e:
        print(f"Script failed: {' '.join(arg)}", file=sys.stderr)
        print("STDOUT:\n", e.stdout, file=sys.stderr)
        print("STDERR:\n", e.stderr, file=sys.stderr)
        sys.exit(e.returncode)  # Exit with the same error code

# ========== Main Script ==========

def main():
    print(f"▶ Running SNODAS ingestion for {ingest_date}...")
    script(["python", "src/ingest/snodas_download.py", "--date", ingest_date])

    print(f"▶ Running NDSI ingestion for {ingest_date}...")
    script(["python", "src/ingest/ndsi_download.py", "--date", ingest_date])

    print("✅ Ingestion complete.")

    script(["python", "src/process/convert.py", "--date", ingest_date])

# ========== Entry Point ==========

if __name__ == "__main__":
    main()