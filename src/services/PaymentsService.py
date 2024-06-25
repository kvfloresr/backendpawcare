import json
from flask_jwt_extended import get_jwt_identity
import pymysql
import requests
import urllib.parse
from flask import jsonify, request
from src.database.db_mysql import get_connection
import uuid
import datetime

def fetch_latest_appointment_details(user_id):
    conn = get_connection()
    try:
        with conn.cursor(pymysql.cursors.DictCursor) as cursor:
            sql = """
            SELECT 
                a.id, a.date, a.time, a.description, 
                cq.category_name, 
                d.first_name, d.last_name, d.phone, d.license_identity
            FROM Appointments a
            JOIN CategoryQuotes cq ON a.category_id = cq.id
            JOIN Doctors d ON a.doctor_id = d.id
            WHERE a.user_id = %s
            ORDER BY a.date DESC, a.time DESC
            LIMIT 1
            """
            cursor.execute(sql, (user_id,))
            result = cursor.fetchone()
            if result:
                appointment_date = result['date']
                appointment_time = result['time']
                return {
                    'appointment_id': result['id'],
                    'date': appointment_date.strftime("%Y-%m-%d") if isinstance(appointment_date, datetime.date) else str(appointment_date),
                    'time': appointment_time.strftime("%H:%M") if isinstance(appointment_time, datetime.time) else str(appointment_time),
                    'description': result['description'],
                    'category_name': result['category_name'],
                    'doctor_name': f"{result['first_name']} {result['last_name']}",
                    'doctor_phone': result['phone'],
                    'doctor_license': result['license_identity']
                }
    finally:
        conn.close()



def generate_payment_number_uuid():
    return str(uuid.uuid4())

def fetch_user_data(user_id):
    conn = get_connection()
    try:
        with conn.cursor(pymysql.cursors.DictCursor) as cursor:
            cursor.execute("SELECT phone, email, first_name, last_name, license_identity FROM Users WHERE id = %s", (user_id,))
            return cursor.fetchone()
    finally:
        conn.close()


def generate_qr(payment_data):
    try:
        user_data = fetch_user_data(payment_data['user_id'])
        appointment_details = fetch_latest_appointment_details(payment_data['user_id']) 
        if not user_data or not appointment_details:
            return {"success": False, "message": "Usuario o cita no encontrados"}

        phone = user_data['phone']
        email = user_data['email']
        first_name = user_data['first_name']
        last_name = user_data['last_name']
        license_identity = user_data['license_identity']

        headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
            'TokenSecret': '9E7BC239DDC04F83B49FFDA5',
            'TokenService': '51247fae280c20410824977b0781453df59fad5b23bf2a0d14e884482f91e09078dbe5966e0b970ba696ec4caf9aa5661802935f86717c481f1670e63f35d5041c31d7cc6124be82afedc4fe926b806755efe678917468e31593a5f427c79cdf016b686fca0cb58eb145cf524f62088b57c6987b3bb3f30c2082b640d7c52907',
            'CommerceId': 'd029fa3a95e174a19934857f535eb9427d967218a36ea014b70ad704bc6c8d1c'
        }

        taPedidoDetalle = json.dumps({
            'item': appointment_details['category_name'],
            'doctor': appointment_details['doctor_name'],
            'fecha': appointment_details['date'],
            'hora': appointment_details['time'],
            'precio': '0.01' 
        })

        body = urllib.parse.urlencode({
            'tcCommerceID': 'd029fa3a95e174a19934857f535eb9427d967218a36ea014b70ad704bc6c8d1c',
            'tnMoneda': '1',
            'tnTelefono': phone,
            'tcCorreo': email,
            'tcNombreUsuario': f"{first_name} {last_name}",
            'tnCiNit': license_identity,
            'tcNroPago': payment_data['tcNroPago'],  
            'tnMontoClienteEmpresa': '0.01',
            'tcUrlCallBack': 'https://apipawcare.onrender.com/payment/callback',
            'tcUrlReturn': '',
            'taPedidoDetalle': taPedidoDetalle
        })

        response = requests.post('https://serviciostigomoney.pagofacil.com.bo/api/servicio/generarqrv2', headers=headers, data=body)

        if response.status_code == 200:
            response_data = response.json()
            if 'values' in response_data and response_data['values']:
                parts = response_data['values'].split(';')
                if len(parts) > 1:
                    qr_base64 = json.loads(parts[1])['qrImage']
                    return {"success": True, "qrImage": f"data:image/png;base64,{qr_base64}"}
                else:
                    return {"success": False, "message": "QR base64 no encontrado en la respuesta."}
            else:
                return {"success": False, "message": "La respuesta del servidor no contiene 'values' o es incorrecta."}
        else:
            return {"success": False, "message": f"Error al generar QR con PagoFácil: {response.text}"}
    except Exception as e:
        return {"success": False, "message": f"Error inesperado al generar QR: {str(e)}"}



def payment_callback():
    data = request.get_json()
    print("Datos recibidos en la consulta (query):", data)

    if not data:
        return jsonify({'error': 1, 'status': 0, 'message': 'Datos no proporcionados'}), 400

    PedidoID = data.get('PedidoID')
    Fecha = data.get('Fecha')
    Hora = data.get('Hora')
    MetodoPago = data.get('MetodoPago')
    Estado = data.get('Estado')

    if not all([PedidoID, Fecha, Hora, MetodoPago, Estado]):
        missing = {
            'PedidoID': not bool(PedidoID),
            'Fecha': not bool(Fecha),
            'Hora': not bool(Hora),
            'MetodoPago': not bool(MetodoPago),
            'Estado': not bool(Estado),
        }
        return jsonify({'error': 1, 'status': 0, 'message': 'Faltan datos necesarios', 'missing': missing}), 400

    try:
        conn = get_connection()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute("SELECT * FROM Payments WHERE PedidoID = %s", (PedidoID,))
        order = cursor.fetchone()

        if not order:
            print("No se encontró ninguna orden con el PedidoID:", PedidoID)
            return jsonify({'error': 1, 'status': 0, 'message': 'Orden no encontrada'}), 404

        if Estado == '2':  
            cursor.execute("""
                UPDATE Payments SET statusPay = True, paymentDetails = %s, Estado = 'confirmado' WHERE PedidoID = %s
            """, (json.dumps(data), PedidoID))

            cursor.execute("""
                UPDATE Appointments SET status_appointments = 'confirmada' WHERE id = %s
            """, (order['appointment_id'],))
            
            conn.commit()
            return jsonify({'error': 0, 'status': 1, 'message': 'Pago confirmado desde CallBack', 'values': True}), 200
        else:
            cursor.execute("""
                UPDATE Payments SET Estado = 'no completado' WHERE PedidoID = %s
            """, (PedidoID,))
            conn.commit()
            return jsonify({'error': 1, 'status': 0, 'message': 'Pago no completado', 'values': False}), 200

    except Exception as e:
        print(f"Error al procesar el pago: {str(e)}")
        return jsonify({'error': 1, 'status': 0, 'message': 'Error interno del servidor: ' + str(e)}), 500
    finally:
        cursor.close()
        conn.close()
