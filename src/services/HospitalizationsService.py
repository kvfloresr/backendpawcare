import pymysql.cursors
from src.database.db_mysql import get_connection

class HospitalizationService:
    
    @staticmethod
    def add_hospitalization(data):
        conn = get_connection()
        try:
            with conn.cursor() as cursor:
                cursor.execute("SELECT id FROM Pets WHERE name = %s", (data['pet_name'],))
                result = cursor.fetchone()
                if result is None:
                    raise ValueError(f"No pet found with name {data['pet_name']}")

                pet_id = result[0]

                cursor.execute(
                    "INSERT INTO Hospitalizations (pet_id, start_date, end_date, reason, observations, status_hospitalization, status_view) VALUES (%s, %s, %s, %s, %s, %s, %s)",
                    (pet_id, data['start_date'], data['end_date'], data['reason'], data['observations'], 'Observacion', 'Visible')
                )
                conn.commit()
        finally:
            conn.close()
        return True

    @staticmethod
    def edit_hospitalization(hospitalization_id, data):
        conn = get_connection()
        try:
            with conn.cursor() as cursor:
                cursor.execute("SELECT id FROM Pets WHERE id = %s", (data['pet_id'],))
                if cursor.fetchone() is None:
                    raise ValueError(f"No pet found with id {data['pet_id']}")

                cursor.execute(
                    "UPDATE Hospitalizations SET pet_id=%s, start_date=%s, end_date=%s, reason=%s, observations=%s, status_hospitalization=%s, status_view=%s WHERE id=%s",
                    (data['pet_id'], data['start_date'], data['end_date'], data['reason'], data['observations'], 'Observacion', 'Visible', hospitalization_id)
                )
                conn.commit()
                if cursor.rowcount == 0:
                    raise ValueError('Hospitalization not found')
        finally:
            conn.close()
        return True

    @staticmethod
    def delete_hospitalization(hospitalization_id):
        conn = get_connection()
        try:
            with conn.cursor() as cursor:
                cursor.execute("UPDATE Hospitalizations SET status_view = 'No visible' WHERE id = %s", (hospitalization_id,))
                conn.commit()
                if cursor.rowcount == 0:
                    raise ValueError('User not found')
        finally:
            conn.close()
        return True
    
    @staticmethod
    def finish_hospitalizations(hospitalization_id):
        conn = get_connection()
        try:
            with conn.cursor() as cursor:
                cursor.execute("UPDATE Hospitalizations SET status_hospitalization = 'Finalizado' WHERE id = %s", (hospitalization_id,))
                conn.commit()
                if cursor.rowcount == 0:
                    raise ValueError('User not found')
        finally:
            conn.close()
        return True

    @staticmethod
    def get_all_hospitalizations():
        conn = get_connection()
        try:
            with conn.cursor(pymysql.cursors.DictCursor) as cursor:
                cursor.execute("SELECT * FROM Hospitalizations WHERE status_view <> 'No Visible'")
                hospitalizations_list = cursor.fetchall()
                return hospitalizations_list
        finally:
            conn.close()
    
    @staticmethod
    def get_hospitalizations_by_pet(pet_id):
        conn = get_connection()
        try:
            with conn.cursor(pymysql.cursors.DictCursor) as cursor:
                cursor.execute("SELECT * FROM Hospitalizations WHERE pet_id = %s AND status_view <> 'No Visible'", (pet_id,))
                hospitalizations_list = cursor.fetchall()
                return hospitalizations_list
        finally:
            conn.close()

