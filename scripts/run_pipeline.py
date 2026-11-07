from pathlib import Path
import subprocess
import sys
import shutil

BASE_DIR = Path(__file__).resolve().parents[1]
DBT_DIR = BASE_DIR / "banking_analytics"

PIPELINE_STEPS = [
    ("Load raw dataset", [sys.executable, "scripts/load_dataset.py"], BASE_DIR),
    ("Validate data quality", [sys.executable, "src/validation/data_quality.py"], BASE_DIR),
    ("Build Silver layer", [sys.executable, "src/transformation/build_silver.py"], BASE_DIR),
    ("Build Gold layer", [sys.executable, "src/transformation/build_gold.py"], BASE_DIR),
    ("Export Silver to Parquet", [sys.executable, "src/transformation/export_silver_parquet.py"], BASE_DIR),
    ("Run PySpark processing", [sys.executable, "src/transformation/pyspark_processing.py"], BASE_DIR),
    ("Run dbt build and tests", [shutil.which("dbt") or "dbt", "build"], DBT_DIR),
]

def run_pipeline():
    print("\n" + "=" * 60)
    print("BANKING DATA ENGINEERING - FULL PIPELINE")
    print("=" * 60)

    for index, (step_name, command, working_dir) in enumerate(PIPELINE_STEPS, 1):
        print(f"\nSTEP {index}/{len(PIPELINE_STEPS)}: {step_name}")
        print("-" * 60)
        subprocess.run(command, cwd=working_dir, check=True)

    print("\n" + "=" * 60)
    print("ALL PIPELINE STEPS COMPLETED SUCCESSFULLY!")
    print("=" * 60)

if __name__ == "__main__":
    try:
        run_pipeline()
    except subprocess.CalledProcessError as error:
        print(f"\nPIPELINE FAILED: {error}")
        sys.exit(error.returncode)
    except Exception as error:
        print(f"\nUNEXPECTED ERROR: {error}")
        sys.exit(1)
