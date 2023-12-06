UPDATE 
	Actions_log
SET 
	id=?,
	 action_datetime=?,
	 optype=?,
	 category=?,
	 amount=?,
	 comment=?
WHERE 
	{mark_name}={mark_val} ;