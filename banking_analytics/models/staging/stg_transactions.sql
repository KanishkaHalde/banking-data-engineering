SELECT
    transaction_step,
    transaction_type,
    transaction_amount,
    sender_id,
    sender_old_balance,
    sender_new_balance,
    receiver_id,
    receiver_old_balance,
    receiver_new_balance,
    is_fraud,
    is_flagged_fraud,
    processed_at

FROM SILVER_TRANSACTIONS
