from flask_jwt_extended import jwt_required, get_jwt_identity
from src.services.UsersService import UsersService
from src.services.AppointmentsService import AppointmentsService
from flask import Blueprint, request, jsonify, make_response

appointments_blueprint = Blueprint('appointments_blueprint', __name__)

@appointments_blueprint.route('/add', methods=['POST'])
@jwt_required()
def add_appointment_route():
    data = request.get_json()
    user_email = get_jwt_identity()
    user_id = UsersService.get_user_id_by_email(user_email)
    data['user_id'] = user_id

    try:
        result = AppointmentsService.add_appointment(data)
        if result.get('success', False):
            response_object = {
                'status': 'success',
                'message': 'Cita agregada exitosamente.',
                'qrImage': result.get('qrImage')
            }
            return make_response(jsonify(response_object), 201)
        else:
            response_object = {
                'status': 'fail',
                'message': result.get('message', 'La cita fue agregada, pero no se pudo generar el QR.')
            }
            return make_response(jsonify(response_object), 202)
    except Exception as e:
        response_object = {
            'status': 'fail',
            'message': str(e)
        }
        return make_response(jsonify(response_object), 400)
    

@appointments_blueprint.route('/add_appointment_admin', methods=['POST'])
@jwt_required()
def add_appointment_admin():
    data = request.get_json()
    try:
        if AppointmentsService.add_appointment_admin(data):
            response_object = {
                'status': 'success',
                'message': 'Cita agregada exitosamente para el usuario.'
            }
            return make_response(jsonify(response_object), 201)
    except Exception as e:
        print(f"Error: {str(e)}")
        response_object = {
            'status': 'fail',
            'message': str(e)
        }
        return make_response(jsonify(response_object), 400)


@appointments_blueprint.route('/edit/<int:appointment_id>', methods=['PUT'])
@jwt_required()
def edit_appointment(appointment_id):
    data = request.get_json()
    try:
        if AppointmentsService.edit_appointment(appointment_id, data):
            response_object = {
                'status': 'success',
                'message': 'La cita se ha editado exitosamente.'
            }
            return make_response(jsonify(response_object), 200)
    except Exception as e:
        response_object = {
            'status': 'fail',
            'message': f"Error: {str(e)}"
        }
        return make_response(jsonify(response_object), 400)
    

@appointments_blueprint.route('/delete/<int:appointment_id>', methods=['PUT'])
@jwt_required()
def delete_appointment(appointment_id):
    try:
        if AppointmentsService.delete_appointment(appointment_id):
            return jsonify({'message': 'Appointment successfully deleted'}), 200
    except Exception as e:
        return jsonify({'message': str(e), 'status': 'fail'}), 400


@appointments_blueprint.route('/finish/<int:appointment_id>', methods=['PUT'])
@jwt_required()
def finish_appointment(appointment_id):
    try:
        if AppointmentsService.finish_appointment(appointment_id):
            return jsonify({'message': 'Appointment successfully finished'}), 200
    except Exception as e:
        return jsonify({'message': str(e), 'status': 'fail'}), 400

# Usuario
@appointments_blueprint.route('/search', methods=['GET'])
@jwt_required()
def get_all_appointments():
    try:
        appointments = AppointmentsService.get_all_appointments()
        return jsonify({'appointments': appointments}), 200
    except Exception as e:
        return jsonify({'message': str(e), 'status': 'fail'}), 400


@appointments_blueprint.route('/pendingappointment', methods=['GET'])
@jwt_required()
def get_pending_appointments():
    try:
        user_email = get_jwt_identity()
        user_id = UsersService.get_user_id_by_email(user_email)
        if user_id:
            pending_appointments = AppointmentsService.get_pending_appointments(user_id)
            return jsonify({'pending_appointments': pending_appointments}), 200
        else:
            return jsonify({'message': 'User not found', 'status': 'fail'}), 404
    except Exception as e:
        return jsonify({'message': str(e), 'status': 'fail'}), 500


@appointments_blueprint.route('/groomingappointment', methods=['GET'])
@jwt_required()
def get_pending_appointments_peluqueria():
    try:
        user_email = get_jwt_identity()
        user_id = UsersService.get_user_id_by_email(user_email)
        if user_id:
            pending_appointments = AppointmentsService.get_appointments_by_category_grooming(user_id)
            return jsonify({'grooming_appointments': pending_appointments}), 200
        else:
            return jsonify({'message': 'User not found', 'status': 'fail'}), 404
    except Exception as e:
        return jsonify({'message': str(e), 'status': 'fail'}), 500
    

@appointments_blueprint.route('/consultationappointment', methods=['GET'])
@jwt_required()
def get_pending_appointments_consultamedica():
    try:
        user_email = get_jwt_identity()
        user_id = UsersService.get_user_id_by_email(user_email)
        if user_id:
            pending_appointments = AppointmentsService.get_appointments_by_category_consult(user_id)
            return jsonify({'consultation_appointments': pending_appointments}), 200
        else:
            return jsonify({'message': 'User not found', 'status': 'fail'}), 404
    except Exception as e:
        return jsonify({'message': str(e), 'status': 'fail'}), 500


# Administrador
@appointments_blueprint.route('/pendingappointmentadmin', methods=['GET'])
@jwt_required()
def get_all_pending_appointments_admin():
    try:
        pending_appointments = AppointmentsService.get_pending_appointments_admin()
        return jsonify({'pending_appointments_admin': pending_appointments}), 200
    except Exception as e:
        return jsonify({'message': str(e), 'status': 'fail'}), 500

@appointments_blueprint.route('/groomingappointmentadmin', methods=['GET'])
@jwt_required()
def get_all_grooming_appointments_admin():
    try:
        grooming_appointments = AppointmentsService.get_appointments_by_category_grooming_admin()
        return jsonify({'grooming_appointments_admin': grooming_appointments}), 200
    except Exception as e:
        return jsonify({'message': str(e), 'status': 'fail'}), 500
    
@appointments_blueprint.route('/consultationappointmentadmin', methods=['GET'])
@jwt_required()
def get_all_consultation_appointments_admin():
    try:
        consultation_appointments = AppointmentsService.get_appointments_by_category_consult_admin()
        return jsonify({'consultation_appointments_admin': consultation_appointments}), 200
    except Exception as e:
        return jsonify({'message': str(e), 'status': 'fail'}), 500


