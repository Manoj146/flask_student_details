from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token
from extensions import db
from models.teacher import Teacher

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/register", methods=["POST"])
def register():
    data = request.json
    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        return jsonify({"error": "Username and password are required"}), 400

    if Teacher.query.filter_by(username=username).first():
        return jsonify({"error": "Username already exists"}), 400

    teacher = Teacher(username=username, password=password)
    db.session.add(teacher)
    db.session.commit()

    return jsonify({"message": "Teacher registered successfully"}), 201


@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.json
    username = data.get("username")
    password = data.get("password")

    teacher = Teacher.query.filter_by(username=username).first()
    if teacher and teacher.password == password:   
        token = create_access_token(identity=str(teacher.id))
        return jsonify({"token": token})
    return jsonify({"error": "Invalid credentials"}), 401
