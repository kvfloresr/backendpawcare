import pymysql.cursors
from src.database.db_mysql import get_connection
import re

class SpecialtiesService:

    @staticmethod
    def add_specialty(data):
        if not re.fullmatch(r'^[A-Za-záéíóúÁÉÍÓÚñÑüÜ ]+$', data['name']):
            raise ValueError('El nombre solo debe contener letras.')

        conn = get_connection()
        try:
            with conn.cursor() as cursor:
                cursor.execute(
                    "INSERT INTO Specialties (name, description, status_view) VALUES (%s, %s, %s)",
                    (data['name'], data['description'], 'Visible')
                )
                conn.commit()
        finally:
            conn.close()
        return True

    @staticmethod
    def edit_specialty(specialty_id, data):

        if not re.fullmatch(r'^[A-Za-záéíóúÁÉÍÓÚñÑüÜ ]+$', data['name']):
            raise ValueError('El nombre solo debe contener letras.')

        conn = get_connection()
        try:
            with conn.cursor() as cursor:
                cursor.execute(
                    "UPDATE Specialties SET name=%s, description=%s WHERE id=%s",
                    (data.get('name'), data.get('description'), specialty_id)
                )
                conn.commit()
                if cursor.rowcount == 0:
                    raise ValueError('Specialty not found')
        finally:
            conn.close()
        return True

    @staticmethod
    def delete_specialty(specialty_id):
        conn = get_connection()
        try:
            with conn.cursor() as cursor:
                cursor.execute("UPDATE Specialties SET status_view = 'No visible' WHERE id = %s", (specialty_id,))
                conn.commit()
                if cursor.rowcount == 0:
                    raise ValueError('User not found')
        finally:
            conn.close()
        return True

    @staticmethod
    def get_all_specialties():
        conn = get_connection()
        try:
            with conn.cursor(pymysql.cursors.DictCursor) as cursor:
                cursor.execute("SELECT * FROM Specialties WHERE status_view <> 'No Visible'")
                specialties = cursor.fetchall()
                return specialties
        finally:
            conn.close()

    @staticmethod
    def get_specialty_names():
        conn = get_connection()
        try:
            with conn.cursor(pymysql.cursors.DictCursor) as cursor:
                cursor.execute("SELECT id, name FROM Specialties WHERE status_view <> 'No Visible'")
                specialty_data = cursor.fetchall()
                specialty_list = [{'id': specialty['id'], 'name': specialty['name']} for specialty in specialty_data]
            return specialty_list
        finally:
            conn.close()
