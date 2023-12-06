UPDATE 
	Actions_log
SET 
	(Actions_log.id={rid},
	 Actions_log.action_datetime={dt},
	 Actions_log.optype='{op}',
	 Actions_log.category='{cat}',
	 Actions_log.amount={amt},
	 Actions_log.comment='{cmt}')
WHERE 
	{mark_name}={mark_val} ;