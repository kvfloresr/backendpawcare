import pymysql.cursors
from src.database.db_mysql import get_connection
import re

class DoctorsService:

    @staticmethod
    def add_doctor(data):
        if not re.fullmatch(r'^[A-Za-záéíóúÁÉÍÓÚñÑüÜ ]+$', data['first_name']):
            raise ValueError('El nombre solo debe contener letras.')
        if not re.fullmatch(r'^[A-Za-záéíóúÁÉÍÓÚñÑüÜ ]+$', data['last_name']):
            raise ValueError('El apellido solo debe contener letras.')

        conn = get_connection()
        cursor = None
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT id FROM Specialties WHERE id = %s", (data['specialty_id'],))
            if cursor.fetchone() is None:
                raise ValueError('El specialty_id proporcionado no existe.')

            cursor.execute(
                "INSERT INTO Doctors (first_name, last_name, phone, status_view, license_identity, specialty_id) VALUES (%s, %s, %s, %s, %s, %s)",
                (data['first_name'], data['last_name'], data['phone'], 'Visible', data.get('license_identity'), data.get('specialty_id'))
            )
            conn.commit()
        except Exception as e:
            conn.rollback()  
            raise e
        finally:
            if cursor:
                cursor.close()  
            conn.close()
        return True

    @staticmethod
    def edit_doctor(doctor_id, data):
        if not re.fullmatch(r'^[A-Za-záéíóúÁÉÍÓÚñÑüÜ ]+$', data['first_name']):
            raise ValueError('El nombre solo debe contener letras.')
        if not re.fullmatch(r'^[A-Za-záéíóúÁÉÍÓÚñÑüÜ ]+$', data['last_name']):
            raise ValueError('El apellido solo debe contener letras.')

        conn = get_connection()
        try:
            with conn.cursor() as cursor:

                cursor.execute(
                    "UPDATE Doctors SET first_name=%s, last_name=%s, phone=%s, status_view=%s, license_identity=%s, specialty_id=%s WHERE id=%s",
                    (data.get('first_name'), data.get('last_name'), data.get('phone'), 'Visible', data.get('license_identity'), data.get('specialty_id'), doctor_id)
                )
                conn.commit()
                if cursor.rowcount == 0:
                    raise ValueError('Doctor not found')
        finally:
            conn.close()
        return True


    @staticmethod
    def delete_doctor(doctor_id):
        conn = get_connection()
        try:
            with conn.cursor() as cursor:
                cursor.execute("UPDATE Doctors SET status_view = 'No visible' WHERE id = %s", (doctor_id,))
                conn.commit()
                if cursor.rowcount == 0:
                    raise ValueError('User not found')
        finally:
            conn.close()
        return True

    @staticmethod
    def get_all_doctors():
        conn = get_connection()
        try:
            with conn.cursor(pymysql.cursors.DictCursor) as cursor:
                cursor.execute("SELECT * FROM Doctors WHERE status_view <> 'No Visible'")
                doctors = cursor.fetchall()
                return doctors
        finally:
            conn.close()

    @staticmethod
    def get_doctor_names():
        conn = get_connection()
        try:
            with conn.cursor(pymysql.cursors.DictCursor) as cursor:
                cursor.execute("SELECT id, first_name FROM Doctors WHERE status_view <> 'No Visible'")
                doctor_data = cursor.fetchall()
                doctor_list = [{'id': doctor['id'], 'name': doctor['first_name']} for doctor in doctor_data]
            return doctor_list
        finally:
            conn.close()


    @staticmethod
    def get_doctor_by_id(doctor_id):
        conn = get_connection()
        try:
            with conn.cursor() as cursor:
                cursor.execute("SELECT * FROM Doctors WHERE id = %s", (doctor_id,))
                doctor = cursor.fetchone()
                if doctor is None:
                    raise ValueError('Doctor not found')
                return doctor
        finally:
            conn.close()
