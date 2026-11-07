
from pathlib import Path
from pyspark.sql import SparkSession
from pyspark.sql.functions import (
    col,
    count,
    sum,
    avg,
    round,
    when
)

BASE_DIR = Path(__file__).resolve().parents[2]

INPUT_PATH = BASE_DIR / "data" / "processed" / "silver_parquet"
OUTPUT_PATH = BASE_DIR / "data" / "processed" / "spark_gold"


def run_pyspark_pipeline():

    print("=" * 55)
    print("BANKING PYSPARK DATA PIPELINE")
    print("=" * 55)

    if not INPUT_PATH.exists():
        raise FileNotFoundError(f"Input folder not found: {INPUT_PATH}")

    spark = (
        SparkSession.builder
        .appName("BankingDataEngineering")
        .master("local[2]")
        .config("spark.sql.shuffle.partitions", "8")
        .config("spark.driver.bindAddress", "127.0.0.1")
        .getOrCreate()
    )

    spark.sparkContext.setLogLevel("ERROR")

    try:
        print("\nReading partitioned Parquet data...")

        df = spark.read.parquet(str(INPUT_PATH))

        print("\nDATA SCHEMA:")
        df.printSchema()

        total = df.count()
        print(f"\nTotal transactions: {total:,}")

        print("\nTRANSACTION SUMMARY:")

        transaction_summary = (
            df.groupBy("transaction_type")
            .agg(
                count("*").alias("total_transactions"),
                round(sum("transaction_amount"), 2)
                .alias("total_amount"),
                round(avg("transaction_amount"), 2)
                .alias("average_amount")
            )
            .orderBy(col("total_transactions").desc())
        )

        transaction_summary.show(truncate=False)

        print("\nFRAUD ANALYSIS:")

        fraud_summary = (
            df.groupBy("transaction_type")
            .agg(
                count("*").alias("total_transactions"),
                sum(
                    when(col("is_fraud"), 1).otherwise(0)
                ).alias("fraud_transactions")
            )
        )

        fraud_summary.show(truncate=False)

        print("\nSaving Spark outputs...")

        transaction_summary.write.mode("overwrite").parquet(
            str(OUTPUT_PATH / "transaction_summary")
        )

        fraud_summary.write.mode("overwrite").parquet(
            str(OUTPUT_PATH / "fraud_summary")
        )

        print("\nPYSPARK PIPELINE COMPLETED!")
        print(f"Outputs saved in: {OUTPUT_PATH}")

    finally:
        spark.stop()


if __name__ == "__main__":
    run_pyspark_pipeline()
