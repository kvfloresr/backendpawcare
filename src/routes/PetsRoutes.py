from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from src.services.PetsService import PetsService
from src.services.UsersService import UsersService

pets_blueprint = Blueprint('pets_blueprint', __name__)

@pets_blueprint.route('/add', methods=['POST'])
@jwt_required()
def add_pet():
    user_email = get_jwt_identity()
    user_id = UsersService.get_user_id_by_email(user_email)
    data = request.get_json()

    try:
        PetsService.add_pet(data, user_id)
        return jsonify({'message': 'Pet successfully added'}), 201
    except Exception as e:
        return jsonify({'message': str(e), 'status': 'fail'}), 400


@pets_blueprint.route('/add_admin', methods=['POST'])
@jwt_required()
def add_pet_admin():
    data = request.get_json()
    user_email = data['email'] 

    try:
        PetsService.add_pet_admin(data, user_email)
        return jsonify({'message': 'Pet successfully added'}), 201
    except Exception as e:
        return jsonify({'message': str(e), 'status': 'fail'}), 400


@pets_blueprint.route('/edit/<int:pet_id>', methods=['PUT'])
@jwt_required()
def edit_pet(pet_id):
    data = request.get_json()

    try:
        PetsService.edit_pet(pet_id, data)
        return jsonify({'message': 'Pet successfully updated'}), 200
    except Exception as e:
        return jsonify({'message': str(e), 'status': 'fail'}), 400

@pets_blueprint.route('/deleteadmin/<int:pet_id>', methods=['PUT'])
@jwt_required()
def delete_pet_admin(pet_id):
    try:
        if PetsService.delete_pet_admin(pet_id):
            return jsonify({'message': 'Pet successfully deleted'}), 200
    except Exception as e:
        return jsonify({'message': str(e), 'status': 'fail'}), 400

@pets_blueprint.route('/delete/<int:pet_id>', methods=['PUT'])
@jwt_required()
def delete_pet(pet_id):
    try:
        if PetsService.delete_pet(pet_id):
            return jsonify({'message': 'Pet successfully deleted'}), 200
    except Exception as e:
        return jsonify({'message': str(e), 'status': 'fail'}), 400


@pets_blueprint.route('/search_user', methods=['GET'])
@jwt_required()  
def get_all_pets_user():
    try:
        pets = PetsService.get_all_pets()
        return jsonify(pets), 200
    except Exception as e:
        return jsonify({'message': str(e), 'status': 'fail'}), 500

@pets_blueprint.route('/search_admin', methods=['GET'])
@jwt_required()  
def get_all_pets_admin():
    try:
        pets = PetsService.get_all_pets_admin()
        return jsonify(pets), 200
    except Exception as e:
        return jsonify({'message': str(e), 'status': 'fail'}), 500


