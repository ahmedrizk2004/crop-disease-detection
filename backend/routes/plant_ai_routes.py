from flask import Blueprint, request, jsonify
import sys, os, base64, tempfile
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from ai.plant_analyzer import analyze_plant_data, analyze_plant_image, format_analysis_report

ai_bp = Blueprint('ai', __name__)

@ai_bp.route('/analyze-data', methods=['POST'])
def analyze_data():
    try:
        data      = request.get_json()
        crop_type = data.get('crop_type', 'Unknown')
        symptoms  = data.get('symptoms', [])
        conditions= data.get('conditions', {})

        result = analyze_plant_data(crop_type, symptoms, conditions)
        return jsonify({"success": True, "analysis": result,
                        "report": format_analysis_report(result)}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@ai_bp.route('/analyze-image', methods=['POST'])
def analyze_image():
    try:
        data       = request.get_json()
        image_b64  = data.get('image_base64')
        if not image_b64:
            return jsonify({"error": "No image provided"}), 400

        with tempfile.NamedTemporaryFile(suffix='.jpg', delete=False) as tmp:
            tmp.write(base64.b64decode(image_b64))
            tmp_path = tmp.name

        result = analyze_plant_image(tmp_path)
        os.unlink(tmp_path)
        return jsonify({"success": True, "analysis": result,
                        "report": format_analysis_report(result)}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
