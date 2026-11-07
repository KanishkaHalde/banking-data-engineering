
import duckdb
from pathlib import Path
import shutil
import sys

sys.path.append(str(Path(__file__).resolve().parents[2]))

from config.config import DATABASE_PATH

BASE_DIR = Path(__file__).resolve().parents[2]

OUTPUT_PATH = BASE_DIR / "data" / "processed" / "silver_parquet"


def export_silver_data():

    print("Starting Silver to Parquet export...")

    connection = duckdb.connect(str(DATABASE_PATH), read_only=True)

    try:

        # Remove previous output if it exists
        if OUTPUT_PATH.exists():
            shutil.rmtree(OUTPUT_PATH)

        OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)

        # Export data partitioned by transaction type
        output = OUTPUT_PATH.as_posix()

        connection.execute(f"""
            COPY (
                SELECT *
                FROM SILVER_TRANSACTIONS
            )
            TO '{output}'
            (
                FORMAT PARQUET,
                PARTITION_BY (transaction_type),
                COMPRESSION ZSTD
            )
        """)

        print("\nParquet export completed!")

        files = list(OUTPUT_PATH.rglob("*.parquet"))

        print(f"Parquet files created: {len(files)}")

        print(f"Output location: {OUTPUT_PATH}")

    finally:
        connection.close()


if __name__ == "__main__":
    export_silver_data()
