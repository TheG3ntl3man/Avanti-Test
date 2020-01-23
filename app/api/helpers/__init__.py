
# este es un helper que creé para tomar los records de sql que vienen en una lista y convertirlos en
# un diccionario
# tambien funciona lara lista de records


def record_to_py(sql_record, keys_array, ignoreID=True):
    if ignoreID:
        sql_record = sql_record[1:]

    dictionary = {}

    for i, k in enumerate(keys_array):
        dictionary[k] = sql_record[i]

    return dictionary


def records_to_py(sql_record_arr, keys_array, ignoreID=True):
    my_list = []
    for record in sql_record_arr:
        my_list.append(record_to_py(record, keys_array, ignoreID))

    return my_list
