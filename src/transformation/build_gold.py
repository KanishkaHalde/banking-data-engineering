
import duckdb
from pathlib import Path
import sys

# Project configuration
sys.path.append(str(Path(__file__).resolve().parents[2]))

from config.config import DATABASE_PATH


def build_gold_layer():

    print("=" * 60)
    print("BUILDING GOLD ANALYTICS LAYER")
    print("=" * 60)

    connection = duckdb.connect(str(DATABASE_PATH))

    try:

        # 1. Transaction summary by type
        print("\nCreating GOLD_TRANSACTION_SUMMARY...")

        connection.execute("""
            CREATE OR REPLACE TABLE GOLD_TRANSACTION_SUMMARY AS
            SELECT
                transaction_type,
                COUNT(*) AS total_transactions,
                ROUND(SUM(transaction_amount), 2) AS total_amount,
                ROUND(AVG(transaction_amount), 2) AS average_amount,
                MAX(transaction_amount) AS maximum_amount
            FROM SILVER_TRANSACTIONS
            GROUP BY transaction_type
        """)

        # 2. Daily transaction summary
        print("Creating GOLD_DAILY_SUMMARY...")

        connection.execute("""
            CREATE OR REPLACE TABLE GOLD_DAILY_SUMMARY AS
            SELECT
                transaction_step,
                COUNT(*) AS total_transactions,
                ROUND(SUM(transaction_amount), 2) AS total_amount,
                ROUND(AVG(transaction_amount), 2) AS average_amount
            FROM SILVER_TRANSACTIONS
            GROUP BY transaction_step
            ORDER BY transaction_step
        """)

        # 3. Fraud analysis
        print("Creating GOLD_FRAUD_ANALYSIS...")

        connection.execute("""
            CREATE OR REPLACE TABLE GOLD_FRAUD_ANALYSIS AS
            SELECT
                transaction_type,
                COUNT(*) AS total_transactions,

                SUM(CASE
                    WHEN is_fraud THEN 1
                    ELSE 0
                END) AS fraud_transactions,

                ROUND(
                    100.0 * SUM(CASE
                        WHEN is_fraud THEN 1
                        ELSE 0
                    END) / COUNT(*), 4
                ) AS fraud_percentage,

                ROUND(SUM(CASE
                    WHEN is_fraud THEN transaction_amount
                    ELSE 0
                END), 2) AS fraud_amount

            FROM SILVER_TRANSACTIONS
            GROUP BY transaction_type
        """)

        # 4. Sender and receiver activity
        print("Creating GOLD_ACCOUNT_ACTIVITY...")

        connection.execute("""
            CREATE OR REPLACE TABLE GOLD_ACCOUNT_ACTIVITY AS

            SELECT
                account_id,
                SUM(sent_transactions) AS sent_transactions,
                SUM(received_transactions) AS received_transactions,
                SUM(total_sent_amount) AS total_sent_amount,
                SUM(total_received_amount) AS total_received_amount

            FROM (

                SELECT
                    sender_id AS account_id,
                    COUNT(*) AS sent_transactions,
                    0 AS received_transactions,
                    SUM(transaction_amount) AS total_sent_amount,
                    0 AS total_received_amount

                FROM SILVER_TRANSACTIONS
                GROUP BY sender_id

                UNION ALL

                SELECT
                    receiver_id AS account_id,
                    0 AS sent_transactions,
                    COUNT(*) AS received_transactions,
                    0 AS total_sent_amount,
                    SUM(transaction_amount) AS total_received_amount

                FROM SILVER_TRANSACTIONS
                GROUP BY receiver_id

            ) account_activity

            GROUP BY account_id
        """)

        print("\nALL GOLD TABLES CREATED!")

        # Display Gold table counts
        tables = [
            "GOLD_TRANSACTION_SUMMARY",
            "GOLD_DAILY_SUMMARY",
            "GOLD_FRAUD_ANALYSIS",
            "GOLD_ACCOUNT_ACTIVITY"
        ]

        print("\nGOLD TABLE RECORD COUNTS")

        for table in tables:

            count = connection.execute(
                f"SELECT COUNT(*) FROM {table}"
            ).fetchone()[0]

            print(f"{table}: {count:,}")

        # Display transaction summary
        print("\nTRANSACTION SUMMARY")

        result = connection.execute("""
            SELECT *
            FROM GOLD_TRANSACTION_SUMMARY
            ORDER BY total_transactions DESC
        """).fetchdf()

        print(result.to_string(index=False))

        # Display fraud analysis
        print("\nFRAUD ANALYSIS")

        fraud_result = connection.execute("""
            SELECT *
            FROM GOLD_FRAUD_ANALYSIS
            ORDER BY fraud_transactions DESC
        """).fetchdf()

        print(fraud_result.to_string(index=False))

        print("\nGOLD LAYER COMPLETED SUCCESSFULLY!")

    finally:
        connection.close()


if __name__ == "__main__":
    build_gold_layer()
