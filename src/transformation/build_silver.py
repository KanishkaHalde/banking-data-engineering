
import duckdb
from pathlib import Path
import sys

# Import project configuration
sys.path.append(str(Path(__file__).resolve().parents[2]))

from config.config import DATABASE_PATH


def build_silver_layer():

    print("=" * 60)
    print("BUILDING SILVER DATA LAYER")
    print("=" * 60)

    connection = duckdb.connect(str(DATABASE_PATH))

    try:

        print("\nReading Bronze transaction data...")

        # Create cleaned and standardised Silver table
        connection.execute("""
            CREATE OR REPLACE TABLE SILVER_TRANSACTIONS AS

            SELECT
                CAST(step AS BIGINT) AS transaction_step,

                TRIM(CAST(type AS VARCHAR)) AS transaction_type,

                CAST(amount AS DECIMAL(20, 2)) AS transaction_amount,

                TRIM(CAST(nameOrig AS VARCHAR)) AS sender_id,

                CAST(oldbalanceOrg AS DECIMAL(20, 2))
                    AS sender_old_balance,

                CAST(newbalanceOrig AS DECIMAL(20, 2))
                    AS sender_new_balance,

                TRIM(CAST(nameDest AS VARCHAR)) AS receiver_id,

                CAST(oldbalanceDest AS DECIMAL(20, 2))
                    AS receiver_old_balance,

                CAST(newbalanceDest AS DECIMAL(20, 2))
                    AS receiver_new_balance,

                CAST(isFraud AS BOOLEAN) AS is_fraud,

                CAST(isFlaggedFraud AS BOOLEAN)
                    AS is_flagged_fraud,

                CURRENT_TIMESTAMP AS processed_at

            FROM RAW_TRANSACTIONS

            WHERE step IS NOT NULL
              AND type IS NOT NULL
              AND amount IS NOT NULL
              AND nameOrig IS NOT NULL
              AND nameDest IS NOT NULL
              AND amount >= 0
              AND type IN (
                  'PAYMENT',
                  'TRANSFER',
                  'CASH_OUT',
                  'CASH_IN',
                  'DEBIT'
              )
        """)

        print("Silver table created successfully!")

        # Count Silver records
        silver_count = connection.execute("""
            SELECT COUNT(*)
            FROM SILVER_TRANSACTIONS
        """).fetchone()[0]

        # Count Bronze records
        bronze_count = connection.execute("""
            SELECT COUNT(*)
            FROM RAW_TRANSACTIONS
        """).fetchone()[0]

        rejected_count = bronze_count - silver_count

        print("\nDATA PROCESSING SUMMARY")

        print(f"Bronze records: {bronze_count:,}")
        print(f"Silver records: {silver_count:,}")
        print(f"Rejected records: {rejected_count:,}")

        # Transaction type summary
        print("\nSILVER TRANSACTION SUMMARY")

        summary = connection.execute("""
            SELECT
                transaction_type,
                COUNT(*) AS total_transactions,
                ROUND(SUM(transaction_amount), 2) AS total_amount
            FROM SILVER_TRANSACTIONS
            GROUP BY transaction_type
            ORDER BY total_transactions DESC
        """).fetchdf()

        print(summary.to_string(index=False))

        print("\nSAMPLE SILVER RECORDS")

        sample = connection.execute("""
            SELECT *
            FROM SILVER_TRANSACTIONS
            LIMIT 5
        """).fetchdf()

        print(sample.to_string(index=False))

        print("\nSILVER LAYER COMPLETED SUCCESSFULLY!")

    finally:
        connection.close()


if __name__ == "__main__":
    build_silver_layer()
