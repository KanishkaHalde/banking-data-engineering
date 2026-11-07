
from pathlib import Path
import pandas as pd

# Dataset location
file_path = Path("data/raw/PS_20174392719_1491204439457_log.csv")

print("Checking PaySim dataset...")

if not file_path.exists():
    print("ERROR: Dataset not found!")
    print("Check whether the CSV is inside data/raw/")
    raise SystemExit(1)

print("Dataset found successfully!")

# Read only 10 rows
df = pd.read_csv(file_path, nrows=10)

print("\nDataset columns:")
print(df.columns.tolist())

print("\nFirst 5 records:")
print(df.head())

print("\nDataset information:")
print(df.info())

print("\nDataset verification completed!")
