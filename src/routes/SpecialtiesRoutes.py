from flask import Blueprint, request, jsonify, make_response
from src.services.SpecialtiesService import SpecialtiesService  

specialties_blueprint = Blueprint('specialties_blueprint', __name__)   

@specialties_blueprint.route('/add', methods=['POST'])
def add_specialty():
    data = request.get_json()
    try:
        if SpecialtiesService.add_specialty(data): 
            return make_response(jsonify({'message': 'Specialty successfully added'}), 201)
    except Exception as e:
        return make_response(jsonify({'message': str(e), 'status': 'fail'}), 400)


@specialties_blueprint.route('/edit/<int:specialty_id>', methods=['PUT'])
def edit_specialty(specialty_id):
    data = request.get_json()
    try:
        if SpecialtiesService.edit_specialty(specialty_id, data): 
            return make_response(jsonify({'message': 'Specialty successfully updated'}), 200)
    except Exception as e:
        return make_response(jsonify({'message': str(e), 'status': 'fail'}), 400)


@specialties_blueprint.route('/delete/<int:specialty_id>', methods=['PUT'])
def delete_specialty(specialty_id):
    try:
        if SpecialtiesService.delete_specialty(specialty_id):  
            return make_response(jsonify({'message': 'Specialty successfully deleted'}), 200)
    except Exception as e:
        return make_response(jsonify({'message': str(e), 'status': 'fail'}), 400)


@specialties_blueprint.route('/search', methods=['GET'])
def get_all_specialties_route():
    try:
        specialties = SpecialtiesService.get_all_specialties()  
        return make_response(jsonify(specialties), 200)
    except Exception as e:
        return make_response(jsonify({'message': str(e), 'status': 'fail'}), 500)

@specialties_blueprint.route('/namespecialties', methods=['GET'])
def get_species_names_route():
    try:
        species_names = SpecialtiesService.get_specialty_names()
        return jsonify({'specialties_names': species_names}), 200
    except Exception as e:
        return make_response(jsonify({'message': str(e), 'status': 'fail'}), 500)