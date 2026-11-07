
from pathlib import Path
import duckdb
import sys

# Import project configuration
sys.path.append(str(Path(__file__).resolve().parent.parent))

from config.config import DATABASE_PATH, DATASET_PATH

def load_banking_dataset():

    print("=" * 55)
    print("BANKING DATA ENGINEERING - DATABASE LOADER")
    print("=" * 55)

    # Check dataset availability
    if not DATASET_PATH.exists():
        print(f"ERROR: Dataset not found: {DATASET_PATH}")
        return

    print("\nDataset found!")
    print("Creating DuckDB database...")

    # Create database directory
    DATABASE_PATH.parent.mkdir(parents=True, exist_ok=True)

    # Connect to persistent DuckDB database
    connection = duckdb.connect(str(DATABASE_PATH))

    try:
        print("\nLoading transaction data...")

        # Create raw transaction table directly from CSV
        connection.execute("""
            CREATE OR REPLACE TABLE RAW_TRANSACTIONS AS
            SELECT *
            FROM read_csv_auto(
                ?,
                header = true,
                sample_size = 100000
            )
        """, [str(DATASET_PATH)])

        print("Data loaded successfully!")

        # Count records
        result = connection.execute("""
            SELECT COUNT(*)
            FROM RAW_TRANSACTIONS
        """).fetchone()

        total_records = result[0]

        print(f"\nTotal transactions loaded: {total_records:,}")

        # Display table columns and data types
        print("\nTABLE STRUCTURE:")

        columns = connection.execute("""
            DESCRIBE RAW_TRANSACTIONS
        """).fetchdf()

        print(columns.to_string(index=False))

        # Display first five records
        print("\nFIRST FIVE TRANSACTIONS:")

        sample = connection.execute("""
            SELECT *
            FROM RAW_TRANSACTIONS
            LIMIT 5
        """).fetchdf()

        print(sample.to_string(index=False))

        # Transaction type summary
        print("\nTRANSACTION TYPE SUMMARY:")

        summary = connection.execute("""
            SELECT
                type,
                COUNT(*) AS total_transactions,
                ROUND(SUM(amount), 2) AS total_amount
            FROM RAW_TRANSACTIONS
            GROUP BY type
            ORDER BY total_transactions DESC
        """).fetchdf()

        print(summary.to_string(index=False))

        print("\nDATABASE LOCATION:")
        print(DATABASE_PATH)

        print("\nDATABASE CREATED SUCCESSFULLY!")

    except Exception as error:
        print(f"\nERROR: {error}")
        raise

    finally:
        connection.close()


if __name__ == "__main__":
    load_banking_dataset()
