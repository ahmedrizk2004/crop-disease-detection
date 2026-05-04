from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from backend.models import db, bcrypt
from backend.routes.disease_routes import disease_bp
from backend.routes.yield_routes import yield_bp
from backend.routes.weather_routes import weather_bp
from backend.routes.plant_ai_routes import ai_bp
from backend.routes.auth_routes import auth_bp
import os

def create_app():
    app = Flask(__name__)

    # Database
    db_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "users.db")
    app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{os.path.normpath(db_path)}"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["SECRET_KEY"] = "crop-secret-jwt-2024"

    db.init_app(app)
    bcrypt.init_app(app)

    # Blueprints
    app.register_blueprint(disease_bp, url_prefix="/api/disease")
    app.register_blueprint(yield_bp,   url_prefix="/api/yield")
    app.register_blueprint(weather_bp, url_prefix="/api/weather")
    app.register_blueprint(ai_bp,      url_prefix="/api/ai")
    app.register_blueprint(auth_bp,    url_prefix="/api/auth")

    @app.route("/api/health")
    def health():
        return {"status": "ok", "message": "Crop API running"}

    with app.app_context():
        db.create_all()
        print("Database ready!")

    return app

app = create_app()

if __name__ == "__main__":
    print("Starting Crop Disease Detection API...")
    print("Running on: http://localhost:5000")
    print("Health check: http://localhost:5000/api/health")
    app.run(debug=True, host="0.0.0.0", port=5000)
