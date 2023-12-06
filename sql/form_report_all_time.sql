SELECT 
    optype, 
    category,
    ROUND(SUM(amount), 2) as total_sum
FROM
    Actions_log
GROUP BY
    optype, 
    category;