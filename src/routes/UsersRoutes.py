from flask import Blueprint, request, jsonify, make_response
from src.services.UsersService import UsersService  
from flask_jwt_extended import jwt_required, get_jwt_identity

auth_blueprint = Blueprint('auth_blueprint', __name__)

@auth_blueprint.route('/register', methods=['POST'])
def register():
    data = request.get_json()

    try:
        if UsersService.register_user(data):
            response_object = {
                'status': 'success',
                'message': 'User successfully registered.'
            }
            return make_response(jsonify(response_object), 201)
    except Exception as e:
        response_object = {
            'status': 'fail',
            'message': str(e)
        }
        return make_response(jsonify(response_object), 400)

@auth_blueprint.route('/login', methods=['POST'])
def login():
    data = request.get_json()

    try:
        auth_token = UsersService.authenticate_user(data['email'], data['password'])
        if auth_token:
            response_object = {
                'status': 'success',
                'message': 'Successfully logged in.',
                'auth_token': auth_token
            }
            return make_response(jsonify(response_object), 200)
    except Exception as e:
        response_object = {
            'status': 'fail',
            'message': str(e)
        }
        return make_response(jsonify(response_object), 401)
    
@auth_blueprint.route('/login_admin', methods=['POST'])
def loginadmin():
    data = request.get_json()

    try:
        auth_token, role_name = UsersService.authenticate_user_admin(data['email'], data['password'])
        if auth_token:
            response_object = {
                'status': 'success',
                'message': 'Successfully logged in.',
                'auth_token': auth_token,
                'role_name': role_name  
            }
            return make_response(jsonify(response_object), 200)
    except Exception as e:
        response_object = {
            'status': 'fail',
            'message': str(e)
        }
        return make_response(jsonify(response_object), 401)



@auth_blueprint.route('/users', methods=['GET'])
def get_users():
    try:
        users = UsersService.get_all_users()
        return jsonify({'users': users}), 200
    except Exception as e:
        return jsonify({'message': str(e), 'status': 'fail'}), 400


@auth_blueprint.route('/delete/<int:user_id>', methods=['PUT'])
@jwt_required()
def delete_user(user_id):
    try:
        if UsersService.delete_user(user_id):
            return jsonify({'message': 'User successfully deleted'}),200
    except Exception as e:
        return jsonify({'message': str(e), 'status': 'fail'}), 400

@auth_blueprint.route('/user/pets', methods=['GET'])
@jwt_required()
def get_user_pets():
    try:
        user_email = get_jwt_identity()  
        user_id = UsersService.get_user_id_by_email(user_email)  
        if user_id:
            pets = UsersService.get_pets_by_user_id(user_id)  
            return jsonify({'pets': pets}), 200
        else:
            return jsonify({'message': 'User not found', 'status': 'fail'}), 404
    except Exception as e:
        return jsonify({'message': str(e), 'status': 'fail'}), 500
    

@auth_blueprint.route('/user/logged', methods=['GET'])  
@jwt_required()
def get_user_info():
    try:
        user_data = UsersService.get_logged_in_user_data() 
        if user_data:
            return jsonify(user_data), 200
        else:
            return jsonify({'message': 'User not found', 'status': 'fail'}), 404
    except Exception as e:
        return jsonify({'message': str(e), 'status': 'fail'}), 500

    
    
@auth_blueprint.route('/user/appointments', methods=['GET'])
@jwt_required()
def get_user_appointments():
    try:
        user_email = get_jwt_identity()  
        user_id = UsersService.get_user_id_by_email(user_email)  
        if user_id:
            appointments = UsersService.get_all_appointments_by_user_id(user_id)  
            return jsonify({'appointments': appointments}), 200
        else:
            return jsonify({'message': 'User not found', 'status': 'fail'}), 404
    except Exception as e:
        return jsonify({'message': str(e), 'status': 'fail'}), 500






