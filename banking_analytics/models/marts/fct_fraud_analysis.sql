SELECT
    transaction_type,
    COUNT(*) AS total_transactions,
    SUM(CASE WHEN is_fraud THEN 1 ELSE 0 END) AS fraud_transactions,
    ROUND(
        100.0 * SUM(CASE WHEN is_fraud THEN 1 ELSE 0 END) / COUNT(*),
        2
    ) AS fraud_percentage

FROM {{ ref('stg_transactions') }}

GROUP BY transaction_type
