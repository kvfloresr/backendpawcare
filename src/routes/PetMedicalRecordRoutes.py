from flask import Blueprint, request, jsonify, make_response
from src.services.PetMedicalRecordService import PetMedicalRecordService  

medical_records_blueprint = Blueprint('medical_records_blueprint', __name__)   

@medical_records_blueprint.route('/add', methods=['POST'])
def add_medical_record():
    data = request.get_json()
    try:
        if PetMedicalRecordService.add_medical_record(data): 
            return make_response(jsonify({'message': 'Medical record successfully added'}), 201)
    except Exception as e:
        print(f"Error: {str(e)}")
        return make_response(jsonify({'message': str(e), 'status': 'fail'}), 400)

@medical_records_blueprint.route('/edit/<int:record_id>', methods=['PUT'])
def edit_medical_record(record_id):
    data = request.get_json()
    try:
        if PetMedicalRecordService.edit_medical_record(record_id, data): 
            return make_response(jsonify({'message': 'Medical record successfully updated'}), 200)
    except Exception as e:
        return make_response(jsonify({'message': str(e), 'status': 'fail'}), 400)

@medical_records_blueprint.route('/delete/<int:record_id>', methods=['PUT'])
def delete_medical_record(record_id):
    try:
        if PetMedicalRecordService.delete_medical_record(record_id):  
            return make_response(jsonify({'message': 'Medical record successfully deleted'}), 200)
    except Exception as e:
        return make_response(jsonify({'message': str(e), 'status': 'fail'}), 400)

@medical_records_blueprint.route('/finish/<int:record_id>', methods=['PUT'])
def finish_medical_record(record_id):
    try:
        if PetMedicalRecordService.finish_medical_record(record_id):  
            return make_response(jsonify({'message': 'Medical record successfully finished'}), 200)
    except Exception as e:
        return make_response(jsonify({'message': str(e), 'status': 'fail'}), 400)

@medical_records_blueprint.route('/search', methods=['GET'])
def get_all_medical_records():
    try:
        records = PetMedicalRecordService.get_all_medical_records()  
        return make_response(jsonify(records), 200)
    except Exception as e:
        return make_response(jsonify({'message': str(e), 'status': 'fail'}), 500)

@medical_records_blueprint.route('/pet/<int:pet_id>', methods=['GET'])
def get_medical_record_by_pet(pet_id):
    try:
        records = PetMedicalRecordService.get_medical_record_by_pet(pet_id)
        return jsonify({'medical_records': records}), 200
    except Exception as e:
        return make_response(jsonify({'message': str(e), 'status': 'fail'}), 500)
    

