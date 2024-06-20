from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
import re  
from pymysql.cursors import DictCursor
import pymysql.cursors 
from src.database.db_mysql import get_connection

class UsersService:
    
    @staticmethod
    def register_user(data):
        if not re.match(r'^[a-zA-Z0-9_.+-]+@gmail\.com$', data['email']):
            raise ValueError('Solo se permiten correos de Gmail.')

        if len(data['password']) < 6 or not re.search(r'[A-Z]', data['password']) or not re.search(r'[0-9]', data['password']):
            raise ValueError('La contraseña debe tener al menos 6 caracteres, incluir al menos una mayúscula y un número.')

        name_fields = ['first_name', 'last_name']
        for field in name_fields:
            if field in data and not re.fullmatch(r'^[a-zA-ZáéíóúÁÉÍÓÚñÑüÜ ]+$', data[field]):
                raise ValueError(f'El campo {field} solo debe contener letras.')

        conn = get_connection()
        try:
            with conn.cursor() as cursor:
                cursor.execute("SELECT * FROM Users WHERE email = %s", (data['email'],))
                if cursor.fetchone():
                    raise ValueError('User already exists')
            default_status_view = "Visible"
            hashed_password = generate_password_hash(data['password'])

            with conn.cursor() as cursor:
                cursor.execute(
                    "INSERT INTO Users (email, password, first_name, last_name, phone, license_identity, role_id, status_view) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
                    (
                    data['email'],
                    hashed_password,
                    data['first_name'],
                    data['last_name'],
                    data['phone'],
                    data['license_identity'],
                    data['role_id'],  
                    default_status_view  
                )
            )
            conn.commit()
        finally:
            conn.close()
        return True
    
    @staticmethod
    def authenticate_user(email, password):
        conn = get_connection()
        try:
            with conn.cursor() as cursor:
                cursor.execute("SELECT password FROM Users WHERE email = %s", (email,))
            user_record = cursor.fetchone()

            if user_record and check_password_hash(user_record[0], password):
                access_token = create_access_token(identity=email)
                return access_token
            else:
                raise ValueError('Invalid credentials')
        finally:
            conn.close()
            
    @staticmethod
    def authenticate_user_admin(email, password):
        conn = get_connection()
        try:
            with conn.cursor() as cursor:
                cursor.execute("""
                    SELECT u.password, r.role_name 
                    FROM Users u 
                    JOIN Roles r ON u.role_id = r.id 
                    WHERE u.email = %s
                """, (email,))
                user_record = cursor.fetchone()

                if user_record and check_password_hash(user_record[0], password):
                    access_token = create_access_token(identity=email)
                    return access_token, user_record[1]  # Retorna el token y el nombre del rol del usuario
                else:
                    raise ValueError('Invalid credentials')
        finally:
            conn.close()



    @staticmethod
    def get_all_users():
        conn = get_connection()
        try:
            with conn.cursor(pymysql.cursors.DictCursor) as cursor:
                cursor.execute("SELECT id, email, first_name, last_name, phone, role_id, status_view, license_identity FROM Users WHERE Users.status_view <> 'No Visible'")
            users = cursor.fetchall()
            return users
        finally:
            conn.close()

    @staticmethod
    def delete_user(user_id):
        conn = get_connection()
        try:
            with conn.cursor() as cursor:
                cursor.execute("UPDATE Users SET status_view = 'No visible' WHERE id = %s", (user_id,))
                conn.commit()
                if cursor.rowcount == 0:
                    raise ValueError('User not found')
        finally:
            conn.close()
        return True

    @staticmethod
    def get_logged_in_user_data():
        user_email = get_jwt_identity()
        conn = get_connection()
        try:
            with conn.cursor(pymysql.cursors.DictCursor) as cursor:
                cursor.execute("SELECT * FROM Users WHERE email = %s", (user_email,))
                user_data = cursor.fetchone()
            if not user_data:
                return None  
            return user_data  
        finally:
            conn.close()

    @staticmethod
    def get_pets_by_user_id(user_id):
        conn = get_connection()
        try:
            with conn.cursor(pymysql.cursors.DictCursor) as cursor:
                cursor.execute("""
                SELECT Pets.*, Species.name as species_name
                FROM Pets
                INNER JOIN Species ON Pets.species_id = Species.id
                WHERE owner_id = %s AND Pets.status_view <> 'No Visible'
            """, (user_id,))
            pets = cursor.fetchall()
            return pets
        finally:
            conn.close()

    @staticmethod
    def get_user_id_by_email(email):
        conn = get_connection()
        try:
            with conn.cursor(DictCursor) as cursor:
                cursor.execute("SELECT id FROM Users WHERE email = %s AND status_view <> 'No Visible'", (email,))
            result = cursor.fetchone()
            if result:
                return result['id']
            else:
                return None
        finally:
            conn.close()

    @staticmethod
    def get_all_appointments_by_user_id(user_id):
        conn = get_connection()
        try:
            with conn.cursor(pymysql.cursors.DictCursor) as cursor:
                cursor.execute("""
                SELECT * FROM Appointments
                WHERE user_id = %s AND status_view <> 'No Visible'
                """, (user_id,))
                appointments = cursor.fetchall()
                return appointments
        finally:
            conn.close()
