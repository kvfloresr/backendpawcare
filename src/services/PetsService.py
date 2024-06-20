import pymysql.cursors
from src.database.db_mysql import get_connection
import re

class PetsService:

    @staticmethod
    def add_pet(data, logged_user_id): 
        if not re.fullmatch(r'^[A-Za-záéíóúÁÉÍÓÚñÑüÜ ]+$', data['name']):
            raise ValueError('El nombre solo debe contener letras.')
        if not re.fullmatch(r'^[A-Za-záéíóúÁÉÍÓÚñÑüÜ ]+$', data['sex']):
            raise ValueError('El sexo solo debe contener letras.') 
        conn = get_connection()
        
        cursor = None
        try:
            cursor = conn.cursor()  
            cursor.execute("SELECT id FROM Species WHERE id = %s", (data['species_id'],))
            if not cursor.fetchone():
                raise ValueError('Specified species does not exist.')

            cursor.execute(
                "INSERT INTO Pets (owner_id, name, species_id, breed, sex, birth_date, status_view) VALUES (%s, %s, %s, %s, %s, %s, %s)",
                (logged_user_id, data['name'], data['species_id'], data['breed'], data['sex'], data['birth_date'], "Visible")
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
    def add_pet_admin(data, user_email): 
        if not re.fullmatch(r'^[A-Za-záéíóúÁÉÍÓÚñÑüÜ ]+$', data['name']):
            raise ValueError('El nombre solo debe contener letras.')
        if not re.fullmatch(r'^[A-Za-záéíóúÁÉÍÓÚñÑüÜ ]+$', data['sex']):
            raise ValueError('El sexo solo debe contener letras.') 

        conn = get_connection()
        cursor = None
        try:
            cursor = conn.cursor()  
            cursor.execute("SELECT id FROM Users WHERE email = %s", (user_email,))
            user_result = cursor.fetchone()
            if not user_result:
                raise ValueError("No user found with the provided email.")

            user_id = user_result[0]

            cursor.execute("SELECT id FROM Species WHERE id = %s", (data['species_id'],))
            if not cursor.fetchone():
                raise ValueError('Specified species does not exist.')

            cursor.execute(
                "INSERT INTO Pets (owner_id, name, species_id, breed, sex, birth_date, status_view) VALUES (%s, %s, %s, %s, %s, %s, %s)",
                (user_id, data['name'], data['species_id'], data['breed'], data['sex'], data['birth_date'], "Visible")
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
    def delete_pet(pet_id):
        conn = get_connection()
        try:
            with conn.cursor() as cursor:
                cursor.execute("UPDATE Pets SET status_view = 'No visible' WHERE id = %s", (pet_id,))
                if cursor.rowcount == 0:
                    raise ValueError('Pet not found')
                
                
                conn.commit()
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            conn.close()
        return True

    @staticmethod
    def get_all_pets():
        conn = get_connection()
        try:
            with conn.cursor(pymysql.cursors.DictCursor) as cursor:
                cursor.execute("""
                SELECT Pets.*, Species.name AS species_name, Users.email AS owner_email
                FROM Pets
                INNER JOIN Species ON Pets.species_id = Species.id
                INNER JOIN Users ON Pets.owner_id = Users.id
                WHERE Pets.status_view <> 'No Visible'
            """)
            pets = cursor.fetchall()
            for pet in pets:
                del pet['species_id']  
            return pets
        finally:
            conn.close()

    @staticmethod
    def get_all_pets_admin():
        conn = get_connection()
        try:
            with conn.cursor(pymysql.cursors.DictCursor) as cursor:
                cursor.execute("""
                SELECT Pets.id, Pets.name, Pets.birth_date, Pets.sex, Pets.breed, Pets.species_id,
                Species.name AS species_name, Users.email AS owner_email
                FROM Pets
                INNER JOIN Species ON Pets.species_id = Species.id
                INNER JOIN Users ON Pets.owner_id = Users.id
                WHERE Pets.status_view <> 'No Visible'
            """)
            pets = cursor.fetchall()
            for pet in pets:
                del pet['species_id']  
            return pets
        finally:
            conn.close()

    @staticmethod
    def edit_pet(pet_id, data):
        conn = get_connection()
        cursor = None
        try:
            cursor = conn.cursor() 
            cursor.execute("SELECT id FROM Species WHERE id = %s", (data['species_id'],))
            if not cursor.fetchone():
                        raise ValueError('Specified species does not exist.')

            columns = []
            values = []
            for key, value in data.items():
                if key in ['name', 'species_id', 'breed', 'sex', 'birth_date', 'status_view']:  
                    columns.append(f"{key}=%s")
                    values.append(value)

            if columns:
                sql_update = f"UPDATE Pets SET {', '.join(columns)} WHERE id=%s"
                values.append(pet_id)
                cursor.execute(sql_update, tuple(values))
                conn.commit()

            if cursor.rowcount == 0:
                raise ValueError('Pet not found')
        finally:
            conn.close()
        return True

    @staticmethod
    def delete_pet_admin(pet_id):
        conn = get_connection()
        try:
            with conn.cursor() as cursor:
                cursor.execute("UPDATE Pets SET status_view = 'No visible' WHERE id = %s", (pet_id,))
                conn.commit()
                if cursor.rowcount == 0:
                    raise ValueError('User not found')
        finally:
            conn.close()
        return True








