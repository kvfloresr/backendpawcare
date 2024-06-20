from flask import Blueprint, request, jsonify, make_response
from src.services.SpeciesService import SpeciesService  

species_blueprint = Blueprint('species_blueprint', __name__)  


@species_blueprint.route('/add', methods=['POST'])
def add_species():
    data = request.get_json()
    try:
        if SpeciesService.add_species(data): 
            return make_response(jsonify({'message': 'Species successfully added'}), 201)
    except Exception as e:
        return make_response(jsonify({'message': str(e), 'status': 'fail'}), 400)


@species_blueprint.route('/edit/<int:species_id>', methods=['PUT'])
def edit_species(species_id):
    data = request.get_json()
    try:
        if SpeciesService.edit_species(species_id, data): 
            return make_response(jsonify({'message': 'Species successfully updated'}), 200)
    except Exception as e:
        return make_response(jsonify({'message': str(e), 'status': 'fail'}), 400)


@species_blueprint.route('/delete/<int:species_id>', methods=['PUT'])
def delete_species(species_id):
    try:
        if SpeciesService.delete_species(species_id):  
            return make_response(jsonify({'message': 'Species successfully deleted'}), 200)
    except Exception as e:
        return make_response(jsonify({'message': str(e), 'status': 'fail'}), 400)


@species_blueprint.route('/search', methods=['GET'])
def get_all_species():
    try:
        species = SpeciesService.get_all_species()  
        return make_response(jsonify(species), 200)
    except Exception as e:
        return make_response(jsonify({'message': str(e), 'status': 'fail'}), 500)


@species_blueprint.route('/namespecies', methods=['GET'])
def get_species_names_route():
    try:
        species_names = SpeciesService.get_species_names()
        return jsonify({'species_names': species_names}), 200
    except Exception as e:
        return make_response(jsonify({'message': str(e), 'status': 'fail'}), 500)
