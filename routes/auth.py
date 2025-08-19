from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token
from models.teacher import Teacher

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.json
    username = data.get("username")
    password = data.get("password")

    teacher = Teacher.query.filter_by(username=username).first()
    if teacher and teacher.password == password:   # ✅ plain text check
        token = create_access_token(identity=str(teacher.id))
        return jsonify({"token": token})
    return jsonify({"error": "Invalid credentials"}), 401
