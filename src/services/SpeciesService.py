import pymysql.cursors
from src.database.db_mysql import get_connection
import re

class SpeciesService:

    @staticmethod
    def add_species(data):
        if not re.fullmatch(r'^[A-Za-záéíóúÁÉÍÓÚñÑüÜ ]+$', data['name']):
            raise ValueError('El nombre solo debe contener letras.')
        
        conn = get_connection()
        try:
            with conn.cursor() as cursor:
                cursor.execute(
                    "INSERT INTO Species (name, description, status_view) VALUES (%s, %s, %s)",
                    (data['name'], data.get('description', ''), 'Visible')
                )
                conn.commit()
        finally:
            conn.close()
        return True

    @staticmethod
    def edit_species(species_id, data):
        if not re.fullmatch(r'^[A-Za-záéíóúÁÉÍÓÚñÑüÜ ]+$', data['name']):
            raise ValueError('El nombre solo debe contener letras.')
        
        conn = get_connection()
        try:
            with conn.cursor() as cursor:
                cursor.execute(
                    "UPDATE Species SET name=%s, description=%s WHERE id=%s",
                    (data['name'], data.get('description', ''), species_id)
                )
                conn.commit()
                if cursor.rowcount == 0:
                    raise ValueError('Species not found')
        finally:
            conn.close()
        return True

    @staticmethod
    def delete_species(species_id):
        conn = get_connection()
        try:
            with conn.cursor() as cursor:
                cursor.execute("UPDATE Species SET status_view = 'No visible' WHERE id = %s", (species_id,))
                conn.commit()
                if cursor.rowcount == 0:
                    raise ValueError('User not found')
        finally:
            conn.close()
        return True

    @staticmethod
    def get_all_species():
        conn = get_connection()
        try:
            with conn.cursor(pymysql.cursors.DictCursor) as cursor:
                cursor.execute("SELECT * FROM Species WHERE status_view <> 'No Visible'")
                species_list = cursor.fetchall()
                return species_list
        finally:
            conn.close()

    @staticmethod
    def get_species_names():
        conn = get_connection()
        try:
            with conn.cursor(pymysql.cursors.DictCursor) as cursor:
                cursor.execute("SELECT id, name FROM Species WHERE status_view <> 'No Visible'")
                species_data = cursor.fetchall()
                species_list = [{'id': species['id'], 'name': species['name']} for species in species_data]
            return species_list
        finally:
            conn.close()
