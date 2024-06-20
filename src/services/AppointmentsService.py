import json
import pymysql.cursors
from src.database.db_mysql import get_connection
from src.services.PaymentsService import generate_qr
import uuid

def generate_payment_number_uuid():
    return str(uuid.uuid4())

class AppointmentsService:
    
    @staticmethod
    def add_appointment(data):
        conn = get_connection()
        try:
            with conn.cursor(pymysql.cursors.DictCursor) as cursor:
                cursor.execute(
                    "SELECT COUNT(*) FROM Pets WHERE id = %s AND owner_id = %s",
                    (data['pet_id'], data['user_id'])
                )
                pet_count = cursor.fetchone()
                if not pet_count or pet_count['COUNT(*)'] == 0:
                    raise ValueError("La mascota no pertenece al usuario.")

                time_str = data['time']
                minutes = int(time_str.split(':')[1])
                if minutes % 20 != 0:
                    raise ValueError("Los minutos deben ser múltiplos de 20 (ej: 00, 20, 40)")

                cursor.execute(
                    "SELECT COUNT(*) FROM Appointments WHERE date = %s AND time = %s",
                    (data['date'], data['time'])
                )
                appointment_count = cursor.fetchone()
                if appointment_count and appointment_count['COUNT(*)'] > 0:
                    raise ValueError("Ya existe una cita reservada para esta fecha y hora.")

                cursor.execute(
                    "INSERT INTO Appointments (user_id, pet_id, doctor_id, date, time, description, status_appointments, category_id, status_view) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)",
                    (data['user_id'], data['pet_id'], data['doctor_id'], data['date'], data['time'], data['description'], data.get('status_appointments', 'Pendiente'), data['category_id'], data.get('status_view', 'Visible'))
                )
                appointment_id = cursor.lastrowid
                conn.commit()

                print(f"Cita agregada con ID: {appointment_id}")

                payment_data = data.get('paymentData', {})
                payment_data['tcNroPago'] = generate_payment_number_uuid() 
                payment_data.update({
                    'Fecha': data['date'],
                    'Hora': data['time'],
                    'MetodoPago': "pendiente",
                    'Estado': "pendiente",
                    'appointmentID': appointment_id,
                    'user_id': data['user_id']
                })

                qr_response = generate_qr(payment_data)  
                if qr_response['success']:
                    qr_image = qr_response['qrImage']
                    
                    cursor.execute("""
                        INSERT INTO Payments (PedidoID, Fecha, Hora, MetodoPago, Estado, statusPay, paymentDetails, userID, appointment_id)
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                    """, (
                        payment_data['tcNroPago'],
                        payment_data['Fecha'],
                        payment_data['Hora'],
                        payment_data['MetodoPago'],
                        'pendiente',
                        False,
                        json.dumps(payment_data),
                        data['user_id'],
                        appointment_id
                    ))
                    payment_id = cursor.lastrowid
                    cursor.execute("UPDATE Appointments SET payment_id = %s WHERE id = %s", (payment_id, appointment_id))
                    conn.commit()

                    return {"success": True, "qrImage": qr_image}
                else:
                    raise ValueError(qr_response['message'])

        except pymysql.MySQLError as e:
            print(f"MySQL error: {str(e)}")
            return {"success": False, "message": f"MySQL error: {str(e)}"}
        except ValueError as e:
            print(f"Value error: {str(e)}")
            return {"success": False, "message": str(e)}
        except Exception as e:
            print(f"Unexpected error: {str(e)}")
            return {"success": False, "message": f"Error inesperado: {str(e)}"}
        finally:
            if conn and conn.open:
                conn.close()
    
    @staticmethod
    def add_appointment_admin(data):
        conn = get_connection()
        try:
            with conn.cursor() as cursor:
                cursor.execute(
                    "SELECT id FROM Users WHERE email = %s",
                    (data['email'],)
                )
                result = cursor.fetchone()
                if not result:
                    raise ValueError("No se encontró un usuario con ese email.")
                user_id = result[0]

                cursor.execute(
                    "SELECT id FROM Pets WHERE name = %s AND owner_id = %s",
                    (data['pet_name'], user_id)
                )
                pet_result = cursor.fetchone()
                if not pet_result:
                    raise ValueError("No se encontró la mascota con ese nombre para el usuario especificado.")
                pet_id = pet_result[0]

                cursor.execute(
                    "SELECT COUNT(*) FROM Appointments WHERE date = %s AND time = %s",
                    (data['date'], data['time'])
                )
                if cursor.fetchone()[0] > 0:
                    raise ValueError("Ya existe una cita reservada para esta fecha y hora.")

                time_str = data['time']
                minutes = int(time_str.split(':')[1])
                if minutes % 20 != 0:
                    raise ValueError("Los minutos deben ser múltiplos de 20 (ej: 00, 20, 40)")

                cursor.execute(
                    "INSERT INTO Appointments (user_id, pet_id, doctor_id, date, time, description, status_appointments, category_id, status_view) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)",
                    (user_id, pet_id, data['doctor_id'], data['date'], data['time'], data['description'], data.get('status_appointments', 'Pendiente'), data['category_id'], data.get('status_view', 'Visible'))
                )
                conn.commit()
        finally:
            conn.close()
        return True

    @staticmethod
    def edit_appointment(appointment_id, data):
        conn = get_connection()
        try:
            with conn.cursor() as cursor:
                time_str = data.get('time')  
                minutes = int(time_str.split(':')[1])  
            
                if minutes % 20 != 0:
                    raise ValueError("Los minutos deben ser múltiplos de 20 (ej: 00, 20, 40)")
            
                cursor.execute(
                    "SELECT id FROM Appointments WHERE date = %s AND time = %s AND id != %s",
                    (data.get('date'), data.get('time'), appointment_id)
                )
                if cursor.fetchone():
                    raise ValueError("Ya existe una cita reservada para esta fecha y hora.")

                cursor.execute(
                    "UPDATE Appointments SET date=%s, time=%s, description=%s, status_appointments=%s, status_view=%s WHERE id=%s",
                    (data.get('date'), data.get('time'), data.get('description'), 'Pendiente', 'Visible', appointment_id)
                )
                conn.commit()
                if cursor.rowcount == 0:
                    raise ValueError('Appointment not found')
        except ValueError as e:
            conn.rollback()
            raise e
        finally:
            conn.close()
        return True

    @staticmethod
    def delete_appointment(appointment_id):
        conn = get_connection()
        try:
            with conn.cursor() as cursor:
                cursor.execute("UPDATE Appointments SET Appointments.status_view = 'No visible' WHERE id = %s", (appointment_id,))
                conn.commit()
                if cursor.rowcount == 0:
                    raise ValueError('User not found')
        finally:
            conn.close()
        return True
    
    @staticmethod
    def finish_appointment(appointment_id):
        conn = get_connection()
        try:
            with conn.cursor() as cursor:
                cursor.execute("UPDATE Appointments SET Appointments.status_appointments = 'Finalizado' WHERE id = %s", (appointment_id,))
                conn.commit()
                if cursor.rowcount == 0:
                    raise ValueError('User not found')
        finally:
            conn.close()
        return True

    @staticmethod
    def get_all_appointments():
        conn = get_connection()
        try:
            with conn.cursor(pymysql.cursors.DictCursor) as cursor:
                cursor.execute("SELECT id, user_id, pet_id, doctor_id, date, TIME_FORMAT(time, '%H:%i:%s') as time, description, status_appointments, category_id FROM Appointments WHERE status_view <> 'No Visible'")
                appointments = cursor.fetchall()
                return appointments
        finally:
            conn.close()

#  Usuario
    @staticmethod
    def get_pending_appointments(user_id):
        conn = get_connection()
        try:
            with conn.cursor(pymysql.cursors.DictCursor) as cursor:
                cursor.execute("""
                    SELECT id, user_id, pet_id, doctor_id, date, TIME_FORMAT(time, '%%H:%%i:%%s') as time, description, status_appointments, category_id
                    FROM Appointments a
                    JOIN Pets p ON a.pet_id 
                    WHERE user_id = %s AND status_appointments = 'Pendiente' AND status_view <> 'No Visible'
                    """, (user_id,))
                pending_appointments = cursor.fetchall()
            return pending_appointments
        finally:
            conn.close()

    @staticmethod
    def get_appointments_by_category_grooming(user_id):
        conn = get_connection()
        try:
            with conn.cursor(pymysql.cursors.DictCursor) as cursor:
                cursor.execute("""
                    SELECT a.id, a.user_id, a.pet_id, a.doctor_id, a.date, TIME_FORMAT(a.time, '%%H:%%i:%%s') as time, a.description, a.status_appointments, a.category_id, p.name AS pet_name
                    FROM Appointments a
                    JOIN Pets p ON a.pet_id = p.id
                    WHERE a.user_id = %s AND a.category_id = '3' AND a.status_view <> 'No Visible'
                    """, (user_id,))
                pending_appointments = cursor.fetchall()
            return pending_appointments
        finally:
            conn.close()

    @staticmethod
    def get_appointments_by_category_consult(user_id):
        conn = get_connection()
        try:
            with conn.cursor(pymysql.cursors.DictCursor) as cursor:
                cursor.execute("""
                    SELECT a.id, a.user_id, a.pet_id, a.doctor_id, a.date, TIME_FORMAT(a.time, '%%H:%%i:%%s') as time, a.description, a.status_appointments, a.category_id, p.name AS pet_name
                    FROM Appointments a
                    JOIN Pets p ON a.pet_id = p.id
                    WHERE a.user_id = %s AND a.category_id = '2' AND a.status_view <> 'No Visible'
                    """, (user_id,))
                pending_appointments = cursor.fetchall()
            return pending_appointments
        finally:
            conn.close()

# Admin
    @staticmethod
    def get_pending_appointments_admin():
        conn = get_connection()
        try:
            with conn.cursor(pymysql.cursors.DictCursor) as cursor:
                cursor.execute("""
                    SELECT id, user_id, pet_id, doctor_id, date, TIME_FORMAT(time, '%%H:%%i:%%s') as time, description, status_appointments, category_id
                    FROM Appointments
                    WHERE status_appointments = 'Pendiente' AND status_view <> 'No Visible'
                    """)
                pending_appointments = cursor.fetchall()
            return pending_appointments
        finally:
            conn.close()

    @staticmethod
    def get_appointments_by_category_grooming_admin():
        conn = get_connection()
        try:
            with conn.cursor(pymysql.cursors.DictCursor) as cursor:
                cursor.execute("""
                    SELECT id, user_id, pet_id, doctor_id, date, TIME_FORMAT(time, '%%H:%%i:%%s') as time, description, status_appointments, category_id
                    FROM Appointments
                    WHERE category_id = '3' AND status_view <> 'No Visible'
                    """)
                grooming_appointments = cursor.fetchall()
            return grooming_appointments
        finally:
            conn.close()

    @staticmethod
    def get_appointments_by_category_consult_admin():
        conn = get_connection()
        try:
            with conn.cursor(pymysql.cursors.DictCursor) as cursor:
                cursor.execute("""
                    SELECT id, user_id, pet_id, doctor_id, date, TIME_FORMAT(time, '%%H:%%i:%%s') as time, description, status_appointments, category_id
                    FROM Appointments
                    WHERE category_id = '2' AND status_view <> 'No Visible'
                    """)
                consult_appointments = cursor.fetchall()
            return consult_appointments
        finally:
            conn.close()



