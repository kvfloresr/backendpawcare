import pymysql

def get_connection():
    host = 'roundhouse.proxy.rlwy.net'
    user = 'root'
    password = 'JojYWcfWGDAXdrQvHBzJXGipBMaSCUGU'  
    db = 'railway'     
    port = 34331                

    try:
        conn = pymysql.connect(host=host, user=user, password=password, db=db, port=port)
        print("Conexión exitosa a la base de datos.")
        return conn
    except pymysql.Error as db_error:
        print(f"Error de base de datos: {db_error}")
    except Exception as ex:
        print(f"Error de conexión: {ex}")

