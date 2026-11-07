import pandas as pd
import duckdb

print("Checking project environment...")

data = {
    "transaction_id": [101, 102, 103],
    "amount": [5000, 7500, 3000]
}

df = pd.DataFrame(data)

print("\nSample transaction data:")
print(df)

connection = duckdb.connect(":memory:")

connection.register("transactions", df)

result = connection.execute("""
    SELECT
        COUNT(*) AS total_transactions,
        SUM(amount) AS total_amount
    FROM transactions
""").fetchdf()

print("\nSQL query result:")
print(result)

connection.close()

print("\nSUCCESS: Environment is working!")