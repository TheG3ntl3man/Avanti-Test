# Avanti-Test
Proyecto para la entrevista 

# Notas:
En el modelo 'ohlc_data' se implemento el query que obtiene el valor 'days_return' y el 'stock_name' como se pide en el documento, sin embargo originalmente en el codigo del modelo se pedia el 'stock_id' por lo que hice un archivo 'query.sql' en la carpeta 'models' donde estan ambos querys, uno que obtiene el 'stock_name' y uno que obtiene el 'stock_id'

En 'tests' esta 'test_ohlc.py' en donde se implementa un unit testing bastante basico donde se verifica que la informacion retornada sea correcta cuando se ingresa una cantidad de dias validos y no validos

Tuve que comentar 2 imports en 'app.py'

#from .api.controllers.book_controller import books_controller

#from .api.controllers.stock_controller import stock_controller

Porque en ambos se importa 'cron', intente instalar esta libreria pero no aparece, por lo que asumi que es una libreria creada por uds que no me fue enviada
