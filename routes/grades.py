from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from models.grade import Grade
from extensions import db

grades_bp = Blueprint("grades", __name__)

# POST /grades - Add grade
@grades_bp.route("", methods=["POST"])
@jwt_required()
def add_grade():
    data = request.json
    grade = Grade(student_id=data["student_id"], subject_id=data["subject_id"], score=data["score"])
    db.session.add(grade)
    db.session.commit()
    return jsonify({"message": "Grade added successfully"})

# PUT /grades/<id> - Update grade
@grades_bp.route("/<int:id>", methods=["PUT"])
@jwt_required()
def update_grade(id):
    grade = Grade.query.get_or_404(id)
    data = request.json
    grade.score = data.get("score", grade.score)
    db.session.commit()
    return jsonify({"message": "Grade updated"})
