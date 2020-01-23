"""" Main connection to the postgres database """
import psycopg2
import os
from dotenv import load_dotenv
from typing import List, Dict, Any, Union
from loguru import logger

load_dotenv(verbose=True)

# clase padre de todos los modelos, realiza la conexión a la db y le proporciona unos métodos para
# ejecutar queries y consultar data a las clases hijas, también hace el mapeo de lo que se trae de la db en
# un diccionario de python

environment = os.getenv("FLASK_ENV")
# print('ENVIRONMENT IS ', environment)
DB_PATH = os.getenv("DATABASE_URL") or os.getenv(f"{environment}_Database")
# print('DB PATH IS >>>>>>>>', DB_PATH)


class Database:
    conn = None
    cur = None

    # esto lo cree para permitir convertir la lista que retorna psycopg en un diccionario
    # quienes descienden de esta clase deben implementar el atributo format
    # lo moví de helpers

    # descendant classes must override this attribute
    format = []

    # this convert a list of values in a dictionary, using as keys the elements stored in format
    def _record_to_py(self, sql_record, format: List[str] = None) -> Dict[str, str]:
        dictionary = {}

        _format = ['id'] + self.format if format is None else format
        for i, k in enumerate(_format):
            dictionary[k] = sql_record[i]

        return dictionary

    def _records_to_py(self, sql_record_arr, format: List[str] = None) -> List[Dict[str, Any]]:
        my_list = []
        for record in sql_record_arr:
            my_list.append(self._record_to_py(record, format))

        return my_list

    def __init__(self, db_url: str = DB_PATH):
        try:
            print("connection to > ", db_url)
            self.conn = psycopg2.connect(db_url)
            self.cur = self.conn.cursor()
        except Exception as error:
            print(
                'CANT CONNECT TO THE DB.....PLEASE CHECK THE PARAMETERS..........................')
            print(error)
            exit()

    def fetchone(self, query: str, format: List[str] = None) -> Union[Dict[str, Any], Any]:
        """ equivalente a psycopg2 fetchone pero mapea a un diccionario el resultado"""
        self.cur.execute(query)
        fetched_row = self.cur.fetchone()
        if fetched_row is not None:
            return self._record_to_py(fetched_row, format)
        else:
            return None

    def execute(self, query: str, format: List[str] = None) -> Union[Dict[str, Any], Any]:
        """  Wrapper de psycopg2 execute, util para insertar o modificar"""
        self.cur.execute(query + ' RETURNING *')
        ob = self.cur.fetchone()
        self.conn.commit()
        if ob is not None:
            return self._record_to_py(ob, format)
        else:
            return None

    def fetchall(self, query: str, format: List[str] = None) -> List[Dict[str, Any]]:
        """ equivalente a psycopg2 fetchal pero mapea a un diccionario el resultado"""
        self.cur.execute(query)
        all_data_rows = self.cur.fetchall()
        return self._records_to_py(all_data_rows, format)
