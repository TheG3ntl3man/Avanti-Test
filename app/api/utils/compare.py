import psycopg2
import pandas as pd

__URL = '167.99.126.129'
__ENGINE = 'postgres'
__USER = 'postgres'
DB_DEVELOPMENT = {
    'engine': __ENGINE,
    'user': __USER,
    'password': 'e3923936c089722f1988373857928f55',
    'url': __URL,
    'port': 21901,
    'database_name': 'angkasadbdev'
}

DB_TEST = {
    'engine': __ENGINE,
    'user': __USER,
    'password': '472210d1663b2171b24e0ac3afe0c822',
    'url': __URL,
    'port': 18060,
    'database_name': 'angkasadbtest'
}
DB = {
    'engine': __ENGINE,
    'user': __USER,
    'password': '1bfa56a7be41f28a477bd84e9538583b',
    'url': __URL,
    'port': 24000,
    'database_name': 'angkasadb'
}


def create_cursor(database):
    # Conecting with database

    with psycopg2.connect(database=database['database_name'],
                          user=database['user'],
                          password=database['password'],
                          host=database['url'],
                          port=database['port']) as conn:
        cursor = conn.cursor()
    return cursor


def get_stock(query, columns, database):
    """
    Creating stock dataframes.

    param query: str. values to query on database
    param columns: list. list of columns to create dataframes

    return stock pd.DataFrame

    """
    accept1 = create_cursor(database)
    accept1.execute(query)
    request = accept1.fetchall()
    stock = pd.DataFrame(request, columns=columns)

    return stock


def get_tag(query, database):
    """
    Creating tag values.

    param query: str. Values to query on database
    return tag list
    """
    accept2 = create_cursor(database)
    accept2.execute(query)
    tag = accept2.fetchall()

    return tag


def combine(source, df_db):
    """
    combine two dataframes and add detail colum,
    where explain if values is to add or not.

    source: location of excel dataframes
    df_db: dataframes of db

    return pd.Dataframes
    """
    df_excel = pd.read_excel(source)
    add = df_excel[~df_excel["stock_name"].isin(df_db["stock_name"])].copy()
    delete = df_db[~ df_db["stock_name"].isin(df_excel["stock_name"])].copy()
    add["info"] = "add"
    delete["info"] = "delete"
    df = add.copy()
    df = df.append(delete)

    return df


if __name__ == '__main__':
    # get stock table
    query_stock = "SELECT * FROM stock"
    df_db = get_stock(query=query_stock, columns=["id", "ticker", "stock_name", "exchange"], database=DB)

    # get df from excel
    excel = "prueba_excel.xlsx"

    # get dataframes
    df = combine(excel, df_db)
    print(df)
