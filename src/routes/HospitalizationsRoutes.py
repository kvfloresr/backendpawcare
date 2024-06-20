from flask import Blueprint, request, jsonify, make_response
from src.services.HospitalizationsService import HospitalizationService  

hospitalization_blueprint = Blueprint('hospitalization_blueprint', __name__)  

@hospitalization_blueprint.route('/add', methods=['POST'])
def add_hospitalization():
        data = request.get_json()
        try:
            if HospitalizationService.add_hospitalization(data): 
                return make_response(jsonify({'message': 'Hospitalization successfully added'}), 201)
        except Exception as e:
            return make_response(jsonify({'message': str(e), 'status': 'fail'}), 400)


@hospitalization_blueprint.route('/edit/<int:hospitalization_id>', methods=['PUT'])
def edit_hospitalization(hospitalization_id):
    data = request.get_json()
    try:
        if HospitalizationService.edit_hospitalization(hospitalization_id, data): 
            return make_response(jsonify({'message': 'Hospitalization successfully updated'}), 200)
    except Exception as e:
        return make_response(jsonify({'message': str(e), 'status': 'fail'}), 400)


@hospitalization_blueprint.route('/delete/<int:hospitalization_id>', methods=['PUT'])
def delete_hospitalization(hospitalization_id):
    try:
        if HospitalizationService.delete_hospitalization(hospitalization_id):  
            return make_response(jsonify({'message': 'Hospitalization successfully deleted'}), 200)
    except Exception as e:
        return make_response(jsonify({'message': str(e), 'status': 'fail'}), 400)


@hospitalization_blueprint.route('/search', methods=['GET'])
def get_all_hospitalizations():
    try:
        hospitalizations = HospitalizationService.get_all_hospitalizations()  
        return make_response(jsonify(hospitalizations), 200)
    except Exception as e:
        return make_response(jsonify({'message': str(e), 'status': 'fail'}), 500)


@hospitalization_blueprint.route('/pet/<int:pet_id>', methods=['GET'])
def get_hospitalizations_by_pet(pet_id):
    try:
        hospitalizations = HospitalizationService.get_hospitalizations_by_pet(pet_id)
        return make_response(jsonify(hospitalizations), 200)
    except Exception as e:
        return make_response(jsonify({'message': str(e), 'status': 'fail'}), 400)
    

@hospitalization_blueprint.route('/finish/<int:hospitalization_id>', methods=['PUT'])
def finish_appointment(appointment_id):
    try:
        if HospitalizationService.finish_hospitalizations(appointment_id):
            response_object = {
                'status': 'success',
                'message': 'Appointment successfully finish.'
            }
            return make_response(jsonify(response_object), 200)
    except Exception as e:
        response_object = {
            'status': 'fail',
            'message': str(e)
        }
        return make_response(jsonify(response_object), 400)
