
import psycopg2
from .database import Database

# LOS MODELOS DESCIENDEN DE Database y deben override el atributo format
# este atributo contiene la lista de los campos que se guardan en la db
# y es utilizado por Database para mapear el resultado del query a la db
# en un diccionario de python cuyas claves son los valores de la lista de format


class Book(Database):
    format = ['title', 'description', 'author']

    def __init__(self):
        super(Book, self).__init__()

    def insert(self, title, description, author):
        query = f"""
            INSERT INTO book(title,description,author)
            VALUES ('{title}','{description}','{author}')
            """

        print("inserting ", query)
        self.execute(query)

    def all(self):
        query = "SELECT * FROM BOOK"
        return self.fetchall(query)
