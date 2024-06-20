from flask import Blueprint, request, jsonify, make_response
from src.services.DoctorsService import DoctorsService

doctors_blueprint = Blueprint('doctors_blueprint', __name__)

@doctors_blueprint.route('/add', methods=['POST'])
def add_doctor():
    data = request.get_json()
    try:
        if DoctorsService.add_doctor(data):
            return make_response(jsonify({'message': 'Doctor successfully added'}), 201)
    except Exception as e:
        return make_response(jsonify({'message': str(e), 'status': 'fail'}), 400)

@doctors_blueprint.route('/edit/<int:doctor_id>', methods=['PUT'])
def edit_doctor(doctor_id):
    data = request.get_json()
    try:
        if DoctorsService.edit_doctor(doctor_id, data):
            return make_response(jsonify({'message': 'Doctor successfully updated'}), 200)
    except Exception as e:
        print(f"Error: {str(e)}")
        return make_response(jsonify({'message': str(e), 'status': 'fail'}), 400)


@doctors_blueprint.route('/delete/<int:doctor_id>', methods=['PUT'])
def delete_doctor(doctor_id):
    try:
        if DoctorsService.delete_doctor(doctor_id):
            return make_response(jsonify({'message': 'Doctor successfully deleted'}), 200)
    except Exception as e:
        return make_response(jsonify({'message': str(e), 'status': 'fail'}), 400)

@doctors_blueprint.route('/search', methods=['GET'])
def get_all_doctors_route():
    try:
        doctors = DoctorsService.get_all_doctors()
        return make_response(jsonify(doctors), 200)
    except Exception as e:
        return make_response(jsonify({'message': str(e), 'status': 'fail'}), 500)

@doctors_blueprint.route('/namesdoctors', methods=['GET'])
def get_doctors_names_route():
    try:
        doctor_names = DoctorsService.get_doctor_names()
        return jsonify({'doctors_names': doctor_names}), 200
    except Exception as e:
        return make_response(jsonify({'message': str(e), 'status': 'fail'}), 500)

@doctors_blueprint.route('/<int:doctor_id>', methods=['GET'])
def get_doctor(doctor_id):
    try:
        doctor = DoctorsService.get_doctor_by_id(doctor_id)
        return jsonify(doctor), 200
    except Exception as e:
        return jsonify({'message': str(e), 'status': 'fail'}), 400
