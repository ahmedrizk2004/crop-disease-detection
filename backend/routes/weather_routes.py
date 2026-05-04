from flask import Blueprint, request, jsonify
import pandas as pd, os

weather_bp = Blueprint('weather', __name__)

# المسار الثابت المباشر
CSV_PATH = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),  # routes/
    "..",   # backend/
    "..",   # CropProject/
    "data", "processed", "weather_data_processed.csv"
)

@weather_bp.route('/summary', methods=['GET'])
def summary():
    try:
        csv_path = os.path.normpath(CSV_PATH)
        df = pd.read_csv(csv_path)
        result = {
            "avg_temperature": round(float(df['temperature_c'].mean()), 2),
            "avg_humidity":    round(float(df['humidity_pct'].mean()), 2),
            "total_rainfall":  round(float(df['rainfall_mm'].sum()), 2),
            "frost_risk_days": int(df['frost_risk'].sum()),
            "regions":         df['region'].unique().tolist()
        }
        return jsonify({"success": True, "data": result}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
