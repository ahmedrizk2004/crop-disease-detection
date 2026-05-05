import sys, os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, BASE_DIR)
os.chdir(BASE_DIR)

from flask import Flask, jsonify
from flask_cors import CORS
from backend.config import Config
from backend.routes.disease_routes import disease_bp
from backend.routes.yield_routes import yield_bp
from backend.routes.plant_ai_routes import ai_bp
from backend.routes.weather_routes import weather_bp

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    CORS(app)

    app.register_blueprint(disease_bp, url_prefix='/api/disease')
    app.register_blueprint(yield_bp,   url_prefix='/api/yield')
    app.register_blueprint(ai_bp,      url_prefix='/api/ai')
    app.register_blueprint(weather_bp, url_prefix='/api/weather')

    @app.route('/api/health', methods=['GET'])
    def health():
        return jsonify({"status": "running", "message": "Crop API running!"}), 200

    return app

if __name__ == "__main__":
    app = create_app()
    port = int(os.environ.get("PORT", 5000))
    print(f"Starting API on port {port}...")
    app.run(host='0.0.0.0', port=port, debug=False)
