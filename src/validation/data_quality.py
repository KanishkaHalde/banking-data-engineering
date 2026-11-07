
import duckdb
from pathlib import Path
import sys

# Import database configuration
sys.path.append(str(Path(__file__).resolve().parents[2]))

from config.config import DATABASE_PATH


def run_data_quality_checks():

    print("=" * 60)
    print("BANKING DATA QUALITY VALIDATION")
    print("=" * 60)

    connection = duckdb.connect(str(DATABASE_PATH))

    try:

        # 1. Total records
        total = connection.execute("""
            SELECT COUNT(*)
            FROM RAW_TRANSACTIONS
        """).fetchone()[0]

        print(f"\nTotal records: {total:,}")

        # 2. Missing values
        missing = connection.execute("""
            SELECT COUNT(*)
            FROM RAW_TRANSACTIONS
            WHERE step IS NULL
               OR type IS NULL
               OR amount IS NULL
               OR nameOrig IS NULL
               OR nameDest IS NULL
        """).fetchone()[0]

        print(f"Records with missing required values: {missing:,}")

        # 3. Negative transaction amounts
        negative = connection.execute("""
            SELECT COUNT(*)
            FROM RAW_TRANSACTIONS
            WHERE amount < 0
        """).fetchone()[0]

        print(f"Negative amount records: {negative:,}")

        # 4. Invalid transaction types
        invalid_types = connection.execute("""
            SELECT COUNT(*)
            FROM RAW_TRANSACTIONS
            WHERE type NOT IN (
                'PAYMENT',
                'TRANSFER',
                'CASH_OUT',
                'DEBIT',
                'CASH_IN'
            )
        """).fetchone()[0]

        print(f"Invalid transaction types: {invalid_types:,}")

        # 5. Duplicate records
        duplicates = connection.execute("""
            SELECT COUNT(*) FROM (
                SELECT step, type, amount, nameOrig,
                       oldbalanceOrg, newbalanceOrig,
                       nameDest, oldbalanceDest,
                       newbalanceDest, isFraud,
                       isFlaggedFraud
                FROM RAW_TRANSACTIONS
                GROUP BY ALL
                HAVING COUNT(*) > 1
            ) duplicate_groups
        """).fetchone()[0]

        print(f"Duplicate record groups: {duplicates:,}")

        # 6. Fraud records (reported separately)
        fraud = connection.execute("""
            SELECT COUNT(*)
            FROM RAW_TRANSACTIONS
            WHERE isFraud = 1
        """).fetchone()[0]

        print(f"Fraud-flagged transactions: {fraud:,}")

        # 7. Balance inconsistencies
        balance_issues = connection.execute("""
            SELECT COUNT(*)
            FROM RAW_TRANSACTIONS
            WHERE
                (
                    type IN ('PAYMENT', 'TRANSFER', 'CASH_OUT', 'DEBIT')
                    AND ABS(
                        oldbalanceOrg - amount - newbalanceOrig
                    ) > 0.01
                )
                OR
                (
                    type = 'CASH_IN'
                    AND ABS(
                        oldbalanceOrg + amount - newbalanceOrig
                    ) > 0.01
                )
        """).fetchone()[0]

        print(f"Potential sender balance inconsistencies: {balance_issues:,}")

        print("\nVALIDATION COMPLETED SUCCESSFULLY!")

    finally:
        connection.close()


if __name__ == "__main__":
    run_data_quality_checks()
