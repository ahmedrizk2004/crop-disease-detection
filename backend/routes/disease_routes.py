from flask import Blueprint, request, jsonify
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from ml_models.disease_detection_cnn import predict_disease

disease_bp = Blueprint('disease', __name__)

@disease_bp.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.get_json()
        required = ['temperature_c','humidity_pct','rainfall_mm',
                    'nitrogen_ppm','phosphorus_ppm','potassium_ppm',
                    'disease_severity','npk_total']
        for f in required:
            if f not in data:
                return jsonify({"error": f"Missing: {f}"}), 400
        return jsonify({"success": True, "data": predict_disease(data)}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
