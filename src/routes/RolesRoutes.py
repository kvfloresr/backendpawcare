from flask import Blueprint, request, jsonify, make_response
from src.services.RolesService import RolesService  

roles_blueprint = Blueprint('roles_blueprint', __name__)

@roles_blueprint.route('/add', methods=['POST'])
def add_role():
    data = request.get_json()
    try:
        if RolesService.add_role(data):
            return make_response(jsonify({'message': 'Role successfully added'}), 201)
    except Exception as e:
        return make_response(jsonify({'message': str(e), 'status': 'fail'}), 400)


@roles_blueprint.route('/edit/<int:role_id>', methods=['PUT'])
def edit_role(role_id):
    data = request.get_json()
    try:
        if RolesService.edit_role(role_id, data):
            return make_response(jsonify({'message': 'Role successfully updated'}), 200)
    except Exception as e:
        return make_response(jsonify({'message': str(e), 'status': 'fail'}), 400)


@roles_blueprint.route('/delete/<int:role_id>', methods=['PUT'])
def delete_role(role_id):
    try:
        if RolesService.delete_role(role_id):
            return make_response(jsonify({'message': 'Role successfully deleted'}), 200)
    except Exception as e:
        return make_response(jsonify({'message': str(e), 'status': 'fail'}), 400)


@roles_blueprint.route('/search', methods=['GET'])
def get_all_roles_route():
    try:
        roles = RolesService.get_all_roles()
        return make_response(jsonify(roles), 200)
    except Exception as e:
        return make_response(jsonify({'message': str(e), 'status': 'fail'}), 500)


@roles_blueprint.route('/namesroles', methods=['GET'])
def get_roles_names_route():
    try:
        roles_names = RolesService.get_roles_names()
        return jsonify({'roles_names': roles_names}), 200
    except Exception as e:
        return make_response(jsonify({'message': str(e), 'status': 'fail'}), 500)