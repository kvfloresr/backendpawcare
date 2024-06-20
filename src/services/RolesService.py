import pymysql.cursors
from src.database.db_mysql import get_connection

class RolesService:

    @staticmethod
    def add_role(data):
        conn = get_connection()
        try:
            with conn.cursor() as cursor:
                cursor.execute(
                    "INSERT INTO Roles (role_name, description, status_view) VALUES (%s, %s, %s)",
                    (data['role_name'], data['description'], 'Visible')
                )
                conn.commit()
        finally:
            conn.close()
        return True

    @staticmethod
    def edit_role(role_id, data):
        conn = get_connection()
        try:
            with conn.cursor() as cursor:
                cursor.execute(
                    "UPDATE Roles SET role_name=%s, description=%s WHERE id=%s",
                    (data.get('role_name'), data.get('description'), role_id)
                )
                conn.commit()
                if cursor.rowcount == 0:
                    raise ValueError('Role not found')
        finally:
            conn.close()
        return True

    @staticmethod
    def delete_role(role_id):
        conn = get_connection()
        try:
            with conn.cursor() as cursor:
                cursor.execute("UPDATE Roles SET status_view = 'No visible' WHERE id = %s", (role_id,))
                conn.commit()
                if cursor.rowcount == 0:
                    raise ValueError('User not found')
        finally:
            conn.close()
        return True

    @staticmethod
    def get_all_roles():
        conn = get_connection()
        try:
            with conn.cursor(pymysql.cursors.DictCursor) as cursor:
                cursor.execute("SELECT * FROM Roles WHERE status_view <> 'No Visible'")
                roles = cursor.fetchall()
                return roles
        finally:
            conn.close()

    @staticmethod
    def get_roles_names():
        conn = get_connection()
        try:
            with conn.cursor(pymysql.cursors.DictCursor) as cursor:
                cursor.execute("SELECT id, role_name FROM Roles WHERE status_view <> 'No Visible'")
                roles_data = cursor.fetchall()
                roles_list = [{'id': role['id'], 'name': role['role_name']} for role in roles_data]
            return roles_list
        finally:
            conn.close()