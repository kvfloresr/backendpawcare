from flask import Blueprint, jsonify, request
from src.services.PaymentsService import generate_qr, payment_callback

payment_blueprint = Blueprint('payment_blueprint', __name__)

@payment_blueprint.route('/generate_qr', methods=['POST'])
def generate_qr_route():
    result = generate_qr()  
    return jsonify(result)

@payment_blueprint.route('/callback', methods=['POST'])
def payment_callback_route():
    return payment_callback()