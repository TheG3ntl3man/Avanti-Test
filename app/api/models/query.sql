-- Query with sotck_id
SELECT ROUND(n.close/o.close-1, 2) AS days_return, o.stock_id
FROM ohlc_data o, (SELECT close, stock_id
					FROM ohlc_data
					WHERE ohlc_timestamp = (SELECT max(ohlc_timestamp) 
											FROM ohlc_data)) n
WHERE o.stock_id = n.stock_id AND
	    o.ohlc_timestamp = ((SELECT max(ohlc_timestamp) 
							FROM ohlc_data) - INTERVAL '7 days');

-- Query with stock_name
SELECT ROUND(n.close/o.close-1, 2) AS days_return, s.stock_name
FROM ohlc_data o, (SELECT close, stock_id
					FROM ohlc_data
					WHERE ohlc_timestamp = (SELECT max(ohlc_timestamp) 
											FROM ohlc_data)) n, stock s
WHERE o.stock_id = n.stock_id AND o.stock_id = s.id AND
		o.ohlc_timestamp = ((SELECT max(ohlc_timestamp) 
							FROM ohlc_data) - INTERVAL '7 days');