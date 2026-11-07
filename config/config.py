
from pathlib import Path

# Get the main project directory
BASE_DIR = Path(__file__).resolve().parent.parent

# Dataset folders
RAW_DATA_DIR = BASE_DIR / "data" / "raw"
PROCESSED_DATA_DIR = BASE_DIR / "data" / "processed"
CURATED_DATA_DIR = BASE_DIR / "data" / "curated"

# DuckDB database location
DATABASE_PATH = BASE_DIR / "data" / "banking.duckdb"

# PaySim dataset filename
DATASET_NAME = "PS_20174392719_1491204439457_log.csv"

# Complete dataset path
DATASET_PATH = RAW_DATA_DIR / DATASET_NAME
