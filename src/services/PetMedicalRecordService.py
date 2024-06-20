import pymysql.cursors
from src.database.db_mysql import get_connection
from pymysql.cursors import DictCursor

class PetMedicalRecordService:

    @staticmethod
    def add_medical_record(data):
        pet_name = data.get('pet_name')
        doctor_id = data.get('doctor_id')

        if not pet_name or not doctor_id:
            raise ValueError("Faltan datos esenciales para el registro.")

        conn = get_connection()
        try:
            with conn.cursor(DictCursor) as cursor: 
                cursor.execute("SELECT id FROM Pets WHERE name = %s", (pet_name,))
                pet_result = cursor.fetchone()
                if not pet_result:
                    raise ValueError("No se encontró la mascota con ese nombre")

                pet_id = pet_result['id']

                cursor.execute("SELECT id FROM Doctors WHERE id = %s", (doctor_id,))
                doctor_result = cursor.fetchone()
                if not doctor_result:
                    raise ValueError("No se encontró el doctor con ese ID")

                cursor.execute(
                    "INSERT INTO Petmedicalrecords (pet_id, doctor_id, date, treatment, diagnosis, notes, status_view, status_petmedical) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
                    (pet_id, doctor_id, data['date'], data['treatment'], data.get('diagnosis', ''), data.get('notes', ''), 'Visible', 'Proceso')
                )
                conn.commit()
        except Exception as e:
            conn.rollback()
            raise ValueError(str(e))
        finally:
            conn.close()
        return {'message': 'Medical record successfully added'}, 201

    
    @staticmethod
    def edit_medical_record(record_id, data):
        conn = get_connection()
        try:
            with conn.cursor() as cursor:
                cursor.execute(
                    "UPDATE Petmedicalrecords SET treatment=%s, notes=%s WHERE id=%s",
                    (data['treatment'], data.get('notes', ''), record_id)
                )
                conn.commit()
                if cursor.rowcount == 0:
                    raise ValueError('Medical record not found')
        finally:
            conn.close()
        return True

    @staticmethod
    def delete_medical_record(record_id):
        conn = get_connection()
        try:
            with conn.cursor() as cursor:
                cursor.execute("UPDATE Petmedicalrecords SET status_view = 'No Visible' WHERE id = %s", (record_id,))
                conn.commit()
                if cursor.rowcount == 0:
                    raise ValueError('Medical record not found')
        finally:
            conn.close()
        return True

    @staticmethod
    def finish_medical_record(record_id):
        conn = get_connection()
        try:
            with conn.cursor() as cursor:
                cursor.execute("UPDATE Petmedicalrecords SET status_petmedical = 'Finalizado' WHERE id = %s", (record_id))
                conn.commit()
                if cursor.rowcount == 0:
                    raise ValueError('Medical record finish')
        finally:
            conn.close()
        return True

    @staticmethod
    def get_all_medical_records():
        conn = get_connection()
        try:
            with conn.cursor(pymysql.cursors.DictCursor) as cursor:
                cursor.execute("SELECT * FROM Petmedicalrecords WHERE status_view <> 'No Visible'")
                records_list = cursor.fetchall()
                return records_list
        finally:
            conn.close()

    @staticmethod
    def get_medical_record_by_pet(pet_id):
        conn = get_connection()
        try:
            with conn.cursor(pymysql.cursors.DictCursor) as cursor:
                cursor.execute("SELECT * FROM Petmedicalrecords WHERE pet_id = %s AND status_view <> 'No Visible'", (pet_id,))
                records_list = cursor.fetchall()
                return records_list
        finally:
            conn.close()
