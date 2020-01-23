import threading

import pandas as pd
import psycopg2
import os
from typing import Any

import requests
from dotenv import load_dotenv
from flask import Flask, request

load_dotenv(verbose=True)

environment = os.getenv("FLASK_ENV")
print('ENVIRONMENT IS ', environment)
DB_PATH = os.getenv("DATABASE_URL") or \
          os.getenv(f"{environment}_Database") or \
          "postgres://postgres:472210d1663b2171b24e0ac3afe0c822@167.99.126.129:18060/angkasadbtest"
print('DB PATH IS >>>>>>>>', DB_PATH)


def create_cursor(db_dns):
    """
        creates a cursor and connection with DB.
    :param database: db dns string.
    :return: (psycopg2.extensions.connection, psycopg2.extensions.cursor)
    """
    # connection = parse_dsn(db_dns)
    conn = psycopg2.connect(dsn=db_dns)
    cursor = conn.cursor()
    return conn, cursor


def clean_tags_from_db(conn, cursor):
    cursor.execute("DELETE FROM stock_tag")
    cursor.execute("DELETE FROM tag")
    conn.commit()


def get_stock(cursor, columns=None):
    """
    Creating stock dataframes.

    param query: str. values to query on database
    param columns: list. list of columns to create dataframes

    return stock pd.DataFrame

    """
    if columns is None:
        columns = ["id", "ticker", "stock_name", "exchange"]

    query_stock = "SELECT * FROM stock"
    cursor.execute(query_stock)
    request = cursor.fetchall()
    stock = pd.DataFrame(request, columns=columns)

    return stock


def compare_dfs(df_excel, df_db):
    """
    combine two dataframes and add detail colum,
    where explain if values is to add or not.

    source: location of excel dataframes
    df_db: dataframes of db

    return pd.Dataframes
    """
    add = df_excel[~df_excel["stock_name"].isin(df_db["stock_name"])].copy()
    delete = df_db[~ df_db["stock_name"].isin(list(df_excel.stock_name))].copy()
    add["info"] = "add"
    delete["info"] = "delete"
    df = add.copy()
    df = df.append(delete)

    return df


def get_tickers_on_excel_document(excel_source: str) -> pd.DataFrame:
    """
        reads an excel document and returns DataFrame.
    :param excel_source: str. Path of excel to read.
    :return:
    """
    datos_tickers = pd.read_excel(excel_source)
    datos_tickers = datos_tickers.rename(columns={"Ticker": "ticker",
                                                  "Name": "stock_name",
                                                  "Exchange": "exchange"})
    return datos_tickers


def stocks_bulk_remove(df, conn, cursor):
    if df.empty:
        return

    delete = df.to_dict('records')
    delete = [stock["ticker"] for stock in delete]
    tickers = str(delete)[1:-1]
    stocks_query = "DELETE FROM stock WHERE ticker IN ({})".format(tickers)
    cursor.execute(stocks_query)
    conn.commit()


def __get_historical_data(ticker_list):
    filename = "{}/yahoo_data/download_data.py".format(os.getcwd())
    arguments = f"--stock={' --stock='.join(ticker_list)}"
    args = f'python {filename} {arguments}'

    download_data_run = threading.Thread(target=os.system, args=(args,))
    download_data_run.daemon = True
    download_data_run.start()


def stocks_bulk_insert(df: pd.DataFrame,
                       conn: psycopg2.extensions.connection,
                       cursor: psycopg2.extensions.cursor) -> Any:
    """
        Inserts all rows of df in the DB.
    :param df: pd.DataFrame. stocks data.
    :param conn: psycopg2.extensions.connection. Connection to DB.
    :param cursor: cursor of DB.
    :return: None.
    """

    if df.empty:
        return

    # iterating in DataFrame rows.
    for index, series in df.iterrows():
        query = "INSERT INTO stock (ticker, stock_name, exchange) " \
                "VALUES ('{}', '{}', '{}') ON CONFLICT DO NOTHING".format(series["ticker"],
                                                                          series["stock_name"],
                                                                          series["exchange"])
        cursor.execute(query)
    conn.commit()

    print(">>> GETTING HISTORICAL DATA")
    ticker_list = list(df["ticker"])
    __get_historical_data(ticker_list)


# required by save_tags_on_db
def __tags_bulk_insert(df: pd.DataFrame,
                       column_name: str,
                       conn: psycopg2.extensions.connection,
                       cursor: psycopg2.extensions.cursor) -> Any:
    """
        Inserts all rows of df in the DB.
    :param df: df with three columns of stock and a column of tag.
    :param column_name: str. The name of tag column.
    :param conn: psycopg2.extensions.connection. Connection to DB.
    :param cursor: cursor of DB.
    :return: None.
    """
    for index, series in df.iterrows():
        if not pd.isnull(series[column_name]):
            query = "INSERT INTO tag (category, tag_name) " \
                    "VALUES ('{}', '{}') " \
                    "ON CONFLICT DO NOTHING".format(column_name, series[column_name])
            cursor.execute(query)
    conn.commit()


# required by save_tags_on_db
def __stock_tags_bulk_insert(df: pd.DataFrame,
                             column_name: str,
                             conn: psycopg2.extensions.connection,
                             cursor: psycopg2.extensions.cursor) -> Any:
    """
        Inserts all tag rows of df in the DB of the relationship between stock and tags.
    :param df: df with three columns of stock and a column of tag.
    :param column_name: str. The name of tag column.
    :param conn: psycopg2.extensions.connection. Connection to DB.
    :param cursor: cursor of DB.
    :return: None.
    """
    for index, series in df.iterrows():
        if not pd.isnull(series[column_name]):
            # first searchs the stock id of row.
            stock_id_query = "SELECT id FROM stock " \
                             "WHERE stock_name = '{}' AND exchange = '{}' AND ticker = '{}'".format(
                series['stock_name'],
                series['exchange'],
                series['ticker'])
            cursor.execute(stock_id_query)
            stock_id = cursor.fetchone()[0]

            # next, searchs the tag id of row.
            tag_id_query = "SELECT id FROM tag WHERE tag_name = '{}' AND category = '{}'".format(series[column_name],
                                                                                                 column_name)
            cursor.execute(tag_id_query)
            tag_id = cursor.fetchone()[0]

            # inserts stock_tag relation using stock_id and tag_id
            query = "INSERT INTO stock_tag (stock_id, tag_id) " \
                    "VALUES ('{}', '{}') ON CONFLICT DO NOTHING".format(stock_id, tag_id)
            cursor.execute(query)
    conn.commit()


def save_tags_on_db(excel_data: pd.DataFrame, conn, cursor) -> Any:
    # saving stocks

    # extracting tag columns
    tag_columns = excel_data.columns
    tag_columns = tag_columns[(tag_columns != "ticker") &
                              (tag_columns != "stock_name") &
                              (tag_columns != "exchange")]
    tags = excel_data[tag_columns]
    tags.apply(lambda x: x.astype(str), axis=1)  # converting fields to string type

    # inserting tag data
    for column in tag_columns:
        __tags_bulk_insert(df=excel_data[["ticker", "stock_name", "exchange", column]],
                           column_name=column,
                           cursor=cursor,
                           conn=conn)
        __stock_tags_bulk_insert(df=excel_data[["ticker", "stock_name", "exchange", column]],
                                 column_name=column,
                                 cursor=cursor,
                                 conn=conn)

    print(">>> ADDED new tag columns")


def build_data_from_excel(excel_file):
    conn, cursor = create_cursor(DB_PATH)

    excel_df = get_tickers_on_excel_document(excel_file)

    # we check and save those new stocks that can be deleted or added
    stocks_df = get_stock(cursor)
    stocks_changed = compare_dfs(excel_df, stocks_df)

    delete = stocks_changed[stocks_changed["info"] == "delete"].copy()[["ticker"]]
    stocks_bulk_remove(df=delete, conn=conn, cursor=cursor)

    added = stocks_changed[stocks_changed["info"] == "add"].copy()[["ticker", "stock_name", "exchange"]]
    stocks_bulk_insert(df=added, conn=conn, cursor=cursor)

    clean_tags_from_db(conn, cursor)

    save_tags_on_db(excel_df, conn, cursor)
