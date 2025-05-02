import argparse
from pathlib import Path

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

# Parse COG file directory from command line
parser = argparse.ArgumentParser(
    description="Start Titiler + FastAPI with configurable data directory."
)
parser.add_argument(
    "-d",
    "--data-dir",
    type=str,
    required=False,
    default=Path("./data/"),
    help="Directory containing STAC catalogue and COG files.",
)
args, _ = parser.parse_known_args()

app = FastAPI()

# Store data directory in app state
app.state.DATA_DIR = args.data_dir.resolve()

# Serve static files from the "static" directory
app.mount("/data", StaticFiles(directory=app.state.DATA_DIR), name="data")
