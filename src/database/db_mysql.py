import pymysql
from dotenv import load_dotenv
import os

load_dotenv()

def get_connection():
    host = os.getenv('DB_HOST')
    user = os.getenv('DB_USER')
    password = os.getenv('DB_PASSWORD')
    db = os.getenv('DB_NAME')
    port = int(os.getenv('DB_PORT'))

    try:
        conn = pymysql.connect(host=host, user=user, password=password, db=db, port=port)
        print("Conexión exitosa a la base de datos.")
        return conn
    except pymysql.Error as db_error:
        print(f"Error de base de datos: {db_error}")
    except Exception as ex:
        print(f"Error de conexión: {ex}")
