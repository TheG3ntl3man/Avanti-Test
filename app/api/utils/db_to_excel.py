import psycopg2
import pandas as pd
import os
from dotenv import load_dotenv
from flask import current_app as app
from cron import ROOT_DIR

# TODO todo este código de db path se puede mover a app y guardarlo en app["DB_PATH"]
load_dotenv(verbose=True)
environment = os.getenv("FLASK_ENV")
print('ENVIRONMENT IS ', environment)
DB = os.getenv("DATABASE_URL") or \
     os.getenv(f"{environment}_Database") or \
     "postgres://postgres:472210d1663b2171b24e0ac3afe0c822@167.99.126.129:18060/angkasadbtest"
print('DB PATH IS >>>>>>>>', DB)


def _create_cursor(db_dns):
    conn = psycopg2.connect(dsn=db_dns)
    cursor = conn.cursor()
    return conn, cursor


def get_stock(query, columns, cursor):
    cursor.execute(query)
    request = cursor.fetchall()
    stock = pd.DataFrame(request, columns=columns)
    return stock


def get_tag(cursor):
    query = "SELECT * FROM stock INNER JOIN stock_tag ON stock.id = stock_tag.stock_id INNER JOIN tag ON " \
            "stock_tag.tag_id = tag.id "
    cursor.execute(query)
    tag = cursor.fetchall()
    return tag


def build_excel_from_db():
    conn, cursor = _create_cursor(db_dns=DB)
    stock = get_stock(query="SELECT * FROM stock", columns=["id", "ticker", "stock_name", "exchange"], cursor=cursor)
    tags = get_tag(cursor=cursor)

    # iteration to create columns value on our DF
    for i in tags:
        new_column = i[8]
        if new_column in ["id", "ticker", "stock_name", "exchange"]:
            print("trying to add an invalid column with same name as default columns, ", new_column)
            continue
        # we add the new columns to our DF with None Values as default
        stock[new_column] = None

    # Adding values to columns created with values of tags
    for i in stock["id"]:
        for j in tags:
            if i == j[0]:
                k = stock["id"][stock["id"] == i].index[0]
                stock[j[8]][k] = j[9]

    stock = stock.drop(stock.columns[[0]], axis=1)

    # return an excel document
    stock.to_excel(os.path.join(ROOT_DIR, app.config["STOCKS_FILE_NAME"]), index=False)
