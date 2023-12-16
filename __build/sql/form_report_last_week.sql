SELECT 
    optype, 
    category,
    ROUND(SUM(amount), 2) as total_sum
FROM
    Actions_log
WHERE
    action_datetime >= date('now', '-7 day')
    AND action_datetime <= date('now', '+1 day')
GROUP BY
    optype, 
    category;