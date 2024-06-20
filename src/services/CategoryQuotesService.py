import pymysql.cursors
from src.database.db_mysql import get_connection

class CategoryQuotesService:

    @staticmethod
    def add_category_quote(category_name):
        conn = get_connection()
        try:
            with conn.cursor() as cursor:
                cursor.execute(
                    "INSERT INTO CategoryQuotes (category_name, status_view) VALUES (%s, %s)",
                    (category_name, 'Visible')
                )
                conn.commit()
        finally:
            conn.close()
        return True


    @staticmethod
    def edit_category_quote(category_id, category_name):
        conn = get_connection()
        try:
            with conn.cursor() as cursor:
                cursor.execute(
                    "UPDATE CategoryQuotes SET category_name=%s, status_view=%s WHERE id=%s",
                    (category_name, 'Visible', category_id)
                )
                conn.commit()
                if cursor.rowcount == 0:
                    raise ValueError('Category not found')
        finally:
            conn.close()
        return True


    @staticmethod
    def delete_category_quote(category_id):
        conn = get_connection()
        try:
            with conn.cursor() as cursor:
                cursor.execute("UPDATE CategoryQuotes SET status_view = 'No visible' WHERE id = %s", (category_id,))
                conn.commit()
                if cursor.rowcount == 0:
                    raise ValueError('User not found')
        finally:
            conn.close()
        return True


    @staticmethod
    def get_all_category_quotes():
        conn = get_connection()
        try:
            with conn.cursor(pymysql.cursors.DictCursor) as cursor:
                cursor.execute("SELECT id, category_name FROM CategoryQuotes WHERE status_view <> 'No Visible'")  
                category_quotes = cursor.fetchall()
                return category_quotes
        finally:
            conn.close()
            
    @staticmethod
    def get_category_names():
        conn = get_connection()
        try:
            with conn.cursor(pymysql.cursors.DictCursor) as cursor:
                cursor.execute("SELECT id, category_name FROM CategoryQuotes WHERE status_view <> 'No Visible'")
                category_data = cursor.fetchall()
                category_list = [{'id': category['id'], 'name': category['category_name']} for category in category_data]
            return category_list
        finally:
            conn.close()

