import psycopg2
import pandas as pd
from .database import Database
from typing import Dict, List, Optional, Any
from loguru import logger


class OHLCData(Database):
    format = ['stock_id', 'open', 'high',
              'low', 'close', 'adj_close',
              'return', 'volume', 'ohlc_timestamp']

    def insert(self, stock_id: int, open: float, high: float,
               low: float, close: float, adj_close: float,
               return_value: float, volume: float, ohlc_timestamp: Optional = None) -> Dict[str, str]:
        """
            insert fields in stock table.
        """
        if ohlc_timestamp is None:
            query = "INSERT INTO stock ({}}) " \
                    "VALUES ({}, {}, {}, {}, {}, {}, {}, {})".format(columns[: -1], stock_id, open, high, low,
                                                                     close, adj_close, return_value, volume)
        else:
            query = "INSERT INTO stock ({}}) " \
                    "VALUES ({}, {}, {}, {}, {}, {}, {}, {}, {})".format(columns, stock_id, open, high, low,
                                                                         close, adj_close, return_value,
                                                                         volume, ohlc_timestamp)
        return self.execute(query)

    def days_return(self, days_number: int) -> List[Dict[str, Any]]:
        """
            :param days_number: int. This is the number of days in the past when we want obtain the old price.
           Days returns is defined as the division of the current price of an action by the price of n days ago.
           represented by the formula:
                    days_returns = current_price / old_price - 1
           Then, this function uses a SQL query to calculate this days returns to ALL stocks at ohlc_data"""

        query = f"""
            SELECT ROUND(n.close/o.close-1, 2) AS days_return, s.stock_name
            FROM ohlc_data o, (SELECT close, stock_id
                                FROM ohlc_data
                                WHERE ohlc_timestamp = (SELECT max(ohlc_timestamp) 
                                                        FROM ohlc_data)) n, stock s
            WHERE o.stock_id = n.stock_id AND o.stock_id = s.id AND
                    o.ohlc_timestamp = ((SELECT max(ohlc_timestamp) 
                                        FROM ohlc_data) - INTERVAL '{days_number} days')
            """

        return self.fetchall(query, format=["days_return", "stock_name"])
