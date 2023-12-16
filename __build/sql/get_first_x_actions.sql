SELECT 
    id, action_datetime, optype, category, amount, comment 
FROM 
    Actions_log
ORDER BY
    action_datetime desc
LIMIT
    60;