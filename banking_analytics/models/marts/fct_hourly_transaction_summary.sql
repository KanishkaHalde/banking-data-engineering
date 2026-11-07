SELECT
    transaction_step,
    transaction_type,

    COUNT(*) AS total_transactions,

    ROUND(SUM(transaction_amount), 2) AS total_amount,

    ROUND(AVG(transaction_amount), 2) AS average_amount,

    SUM(CASE WHEN is_fraud THEN 1 ELSE 0 END) AS fraud_transactions

FROM {{ ref('stg_transactions') }}

GROUP BY
    transaction_step,
    transaction_type
