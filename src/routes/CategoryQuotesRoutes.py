from flask_jwt_extended import jwt_required
from src.services.CategoryQuotesService import CategoryQuotesService
from flask import Blueprint, request, jsonify, make_response

category_quotes_blueprint = Blueprint('category_quotes_blueprint', __name__)


@category_quotes_blueprint.route('/add', methods=['POST'])
@jwt_required()
def add_category_quote():
    data = request.get_json()
    try:
        if CategoryQuotesService.add_category_quote(data['category_name']):
            response_object = {
                'status': 'success',
                'message': 'Category quote added successfully.'
            }
            return make_response(jsonify(response_object), 201)
    except Exception as e:
        response_object = {
            'status': 'fail',
            'message': str(e)
        }
        return make_response(jsonify(response_object), 400)


@category_quotes_blueprint.route('/edit/<int:category_id>', methods=['PUT'])
@jwt_required()
def edit_category_quote(category_id):
    data = request.get_json()
    try:
        if CategoryQuotesService.edit_category_quote(category_id, data['category_name']):
            response_object = {
                'status': 'success',
                'message': 'Category quote successfully edited.'
            }
            return make_response(jsonify(response_object), 200)
    except Exception as e:
        response_object = {
            'status': 'fail',
            'message': str(e)
        }
        return make_response(jsonify(response_object), 400)


@category_quotes_blueprint.route('/delete/<int:category_id>', methods=['PUT'])
@jwt_required()
def delete_category_quote(category_id):
    try:
        if CategoryQuotesService.delete_category_quote(category_id):
            response_object = {
                'status': 'success',
                'message': 'Category quote successfully deleted.'
            }
            return make_response(jsonify(response_object), 200)
    except Exception as e:
        response_object = {
            'status': 'fail',
            'message': str(e)
        }
        return make_response(jsonify(response_object), 400)


@category_quotes_blueprint.route('/search', methods=['GET'])
@jwt_required()
def get_all_category_quotes():
    try:
        category_quotes = CategoryQuotesService.get_all_category_quotes()
        return jsonify({'category_quotes': category_quotes}), 200
    except Exception as e:
        return jsonify({'message': str(e), 'status': 'fail'}), 400
    
@category_quotes_blueprint.route('/names', methods=['GET'])
@jwt_required()
def get_category_names():
    try:
        category_names = CategoryQuotesService.get_category_names()
        return jsonify({'category_names': category_names}), 200
    except Exception as e:
        return jsonify({'message': str(e), 'status': 'fail'}), 400

