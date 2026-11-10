# Banking Data Engineering Project

## Overview
An end-to-end banking data engineering project that processes financial transactions, performs data quality checks, identifies fraudulent transactions, and generates analytical datasets for reporting.

## Technologies Used
- Python – Data ingestion and processing
- Pandas – Data manipulation
- DuckDB – Data storage and SQL transformations
- PySpark – Distributed data processing
- dbt – Data modelling and testing
- Snowflake – Cloud data warehouse integration
- Power BI – Interactive dashboard
- GitHub Actions – Continuous integration

## Project Architecture

Raw CSV Data
      |
      v
Python Data Ingestion
      |
      v
Data Quality Validation
      |
      v
DuckDB (Bronze Layer)
      |
      v
Silver Layer
      |
      v
Gold Layer
      |
      +-----------> PySpark Processing
      |
      +-----------> dbt Models and Tests
      |
      +-----------> Snowflake
      |
      v
Power BI Dashboard

## Dataset
PaySim synthetic financial transaction dataset.

- Total transactions: 6,362,620
- Fraudulent transactions: 8,213
- Transaction types: CASH_IN, CASH_OUT, DEBIT, PAYMENT, TRANSFER

## Data Engineering Workflow
1. Ingested raw banking transaction data using Python.
2. Performed data quality validation.
3. Created Bronze, Silver, and Gold data layers using DuckDB.
4. Exported processed data into partitioned Parquet files.
5. Used PySpark for transaction and fraud analysis.
6. Built analytical models using dbt.
7. Executed dbt tests to validate the models.
8. Loaded Gold datasets into Snowflake using staged CSV files and COPY INTO.
9. Created a Power BI dashboard for transaction and fraud analysis.

## Snowflake Integration
Created and loaded the following Gold tables:
- GOLD_TRANSACTION_SUMMARY
- GOLD_DAILY_SUMMARY
- GOLD_FRAUD_ANALYSIS

## Power BI Dashboard
The dashboard presents:
- Total transactions
- Total transaction amount
- Total fraud transactions
- Transaction amount by transaction type
- Fraud transactions by transaction type
- Daily transaction volume trends

## Data Quality
Validated:
- Missing required values
- Negative transaction amounts
- Invalid transaction types
- Duplicate records

## Testing
dbt build completed successfully with 4 models and 20 tests passing.

## CI/CD
GitHub Actions workflow configured to run Python checks when code is pushed to the repository.

## Repository Structure
```text
banking-data-engineering/
├── config/
├── data/
│   ├── raw/
│   ├── processed/
│   └── powerbi/
├── scripts/
├── src/
│   ├── ingestion/
│   ├── transformation/
│   └── validation/
├── banking_analytics/
│   └── models/
├── tests/
├── .github/
│   └── workflows/
├── requirements.txt
└── README.md
```

## Key Outcomes
- Processed over 6.3 million banking transactions.
- Identified 8,213 fraudulent transactions.
- Built analytical datasets using SQL and PySpark.
- Validated dbt models with automated tests.
- Integrated Gold datasets with Snowflake.
- Developed an interactive Power BI dashboard.
