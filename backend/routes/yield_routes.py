from flask import Blueprint, request, jsonify
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from ml_models.yield_prediction_regression import predict_yield

yield_bp = Blueprint('yield', __name__)

@yield_bp.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.get_json()
        return jsonify({"success": True, "data": predict_yield(data)}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
