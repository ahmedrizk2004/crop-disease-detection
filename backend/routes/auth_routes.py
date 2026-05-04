from flask import Blueprint, request, jsonify
from backend.models import db, User
import jwt, datetime, os

auth_bp = Blueprint("auth", __name__)
SECRET = "crop-secret-jwt-2024"

def make_token(user_id):
    payload = {
        "user_id": user_id,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(days=7)
    }
    return jwt.encode(payload, SECRET, algorithm="HS256")

@auth_bp.route("/register", methods=["POST"])
def register():
    try:
        data     = request.get_json()
        name     = data.get("name", "").strip()
        email    = data.get("email", "").strip().lower()
        password = data.get("password", "")

        if not name or not email or not password:
            return jsonify({"error": "All fields are required"}), 400
        if len(password) < 6:
            return jsonify({"error": "Password must be at least 6 characters"}), 400
        if User.query.filter_by(email=email).first():
            return jsonify({"error": "Email already registered"}), 409

        user = User(name=name, email=email)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()

        token = make_token(user.id)
        return jsonify({"success": True, "token": token, "user": user.to_dict()}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@auth_bp.route("/login", methods=["POST"])
def login():
    try:
        data     = request.get_json()
        email    = data.get("email", "").strip().lower()
        password = data.get("password", "")

        if not email or not password:
            return jsonify({"error": "Email and password are required"}), 400

        user = User.query.filter_by(email=email).first()
        if not user or not user.check_password(password):
            return jsonify({"error": "Invalid email or password"}), 401

        token = make_token(user.id)
        return jsonify({"success": True, "token": token, "user": user.to_dict()}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@auth_bp.route("/me", methods=["GET"])
def me():
    try:
        token = request.headers.get("Authorization", "").replace("Bearer ", "")
        if not token:
            return jsonify({"error": "No token provided"}), 401
        payload = jwt.decode(token, SECRET, algorithms=["HS256"])
        user    = User.query.get(payload["user_id"])
        if not user:
            return jsonify({"error": "User not found"}), 404
        return jsonify({"success": True, "user": user.to_dict()}), 200
    except jwt.ExpiredSignatureError:
        return jsonify({"error": "Token expired, please login again"}), 401
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@auth_bp.route("/reset-password", methods=["POST"])
def reset_password():
    try:
        data     = request.get_json()
        email    = data.get("email", "").strip().lower()
        new_pass = data.get("new_password", "")

        if not email or not new_pass:
            return jsonify({"error": "Email and new password are required"}), 400
        if len(new_pass) < 6:
            return jsonify({"error": "Password must be at least 6 characters"}), 400

        user = User.query.filter_by(email=email).first()
        if not user:
            return jsonify({"error": "Email not found"}), 404

        user.set_password(new_pass)
        db.session.commit()
        return jsonify({"success": True, "message": "Password updated successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
