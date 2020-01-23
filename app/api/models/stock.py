import psycopg2
import pandas as pd
import itertools
from .database import Database
from typing import Dict, List, Any
from .ohlc_data import OHLCData
from loguru import logger
import math


class Stock(Database):
    format = ['ticker', 'stock_name', 'exchange']

    def __init__(self):
        super(Stock, self).__init__()

    def get_stock(self, id: int) -> Dict[str, str]:
        query = "SELECT * FROM stock WHERE id = {}".format(id)
        return self.fetchone(query)

    def insert(self, ticker: str, stock_name: str, exchange: str) -> Dict[str, str]:
        """
            insert fields in stock table.
        """
        query = "INSERT INTO stock (ticker, stock_name, exchange) " \
                "VALUES ('{}', '{}', '{}')".format(ticker, stock_name, exchange)
        return self.execute(query)

    def all(self) -> List[Dict[str, str]]:
        """
            extract all rows of stock table.
        :return: list of tuples. Each tuple contains
        """
        query = "SELECT * FROM stock"
        return self.fetchall(query)

    def update(self, id: int, fields: Dict[str, str]) -> Dict[str, str]:
        keys = fields.keys()
        values = fields.values()
        equalities = ["{} = '{}'".format(key, value) for key, value in zip(keys, values)]
        equalities = ", ".join(equalities)
        query = "UPDATE stock SET {} WHERE id = {}".format(equalities, id)
        return self.execute(query)

    def delete(self, id: int) -> Dict[str, str]:
        query = "DELETE FROM stock WHERE id = {}".format(id)
        return self.execute(query)

    def days_return(self, days_number: int):
        return OHLCData().days_return(days_number=days_number)

    def extract_last_timestamp_stocks(self) -> List[Dict[str, Any]]:
        stock_ohlc_query = "SELECT stock_id, ticker, stock_name, open, high, low, close, return, volume " \
                           "FROM stock S JOIN ohlc_data OD " \
                           "ON S.id = OD.stock_id AND ohlc_timestamp = (SELECT MAX(ohlc_timestamp) FROM ohlc_data) " \
                           "ORDER BY stock_id ASC"
        stock_ohlc = self.fetchall(stock_ohlc_query, format=["id", "ticker", "name", "open",
                                                             "high", "low", "lastclose", "return", "volume"])
        return stock_ohlc

    def extract_stock_tag_by_stocks_ids(self, stocks_ids: List[int]) -> List:
        stock_tag_query = "SELECT stock_id, category, tag_name " \
                          "FROM (tag JOIN stock_tag st " \
                          "ON tag.id = st.tag_id JOIN stock s " \
                          "ON st.stock_id = s.id) WHERE st.stock_id IN ({})" \
                          "ORDER BY stock_id ASC".format(', '.join(str(x) for x in stocks_ids))
        stock_tag = self.fetchall(stock_tag_query, format=["stock_id", "category", "tag_name"])
        return stock_tag

    def extract_stocks(self) -> List[Dict[str, Any]]:
        stock_ohlc = self.extract_last_timestamp_stocks()

        if len(stock_ohlc) < 1:
            return []

        aux_stock_ohlc = pd.DataFrame(stock_ohlc)
        stocks_ids = aux_stock_ohlc["id"].unique()
        stock_tag = self.extract_stock_tag_by_stocks_ids(stocks_ids=stocks_ids)
        if len(stock_tag) > 0:
            stock_tag = pd.DataFrame(stock_tag)
            stocks_ids = stock_tag["stock_id"].unique()

        # Inserting "tag" field to list of dicts
        for i, stock in enumerate(stock_ohlc):
            stock_ohlc[i]["tag"] = []

        # Inserting tag info to stocks with tags.
        if len(stock_tag) > 0:
            for id in stocks_ids:
                index = aux_stock_ohlc[aux_stock_ohlc["id"] == id].index[0]
                stock_ohlc[index]["tag"] = ["{}:{}".format(row["category"], row["tag_name"])
                                            for index, row in stock_tag[stock_tag["stock_id"] == id].iterrows()]

        # casting types from SQL to python types.
        for stock in stock_ohlc:
            stock["id"] = int(stock["id"])
            stock["open"] = float(stock["open"])
            stock["high"] = float(stock["high"])
            stock["low"] = float(stock["low"])
            stock["lastclose"] = float(stock["lastclose"])
            stock["return"] = None if math.isnan(stock["return"]) else float(stock["return"])
            stock["volume"] = float(stock["volume"])
        return stock_ohlc

    def insert_stocks_list(self, stocks_list: List[Dict[str, Any]]):
        example_dict = stocks_list[0]
        columns = ", ".join(list(example_dict.keys()))

        # creating a '(%s, %s, ..., %s)' string
        s_pct_list = [str(tuple(stock.values())) for stock in stocks_list]

        # "unrolling" stock list
        stocks_query = "INSERT INTO stock ({}) VALUES {}".format(columns, ','.join(s_pct_list))
        self.execute(stocks_query)

    def remove_stocks_list(self, tickers):
        tickers = str(tickers)[1:-1]
        stocks_query = "DELETE FROM stock WHERE ticker IN ({})".format(tickers)
        self.execute(stocks_query)
