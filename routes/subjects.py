from flask import Blueprint,request, jsonify
from flask_jwt_extended import jwt_required
from models.grade import Grade
from models.subject import Subject
from extensions import db
from sqlalchemy import func

subjects_bp = Blueprint("subjects", __name__)

@subjects_bp.route("", methods=["POST"])
@jwt_required()
def add_subject():
    data = request.json
    if Subject.query.filter_by(name=data.get("name")).first():
        return jsonify({"error": "Subject already exists"}), 400
    subject = Subject(name=data.get("name"))
    db.session.add(subject)
    db.session.commit()
    return jsonify({"message": "Subject added", "id": subject.id})

# GET /subjects/<id>/grades - Get subject grades + stats
@subjects_bp.route("/<int:id>/grades", methods=["GET"])
@jwt_required()
def subject_grades(id):
    grades = Grade.query.filter_by(subject_id=id).all()
    avg_score = db.session.query(func.avg(Grade.score)).filter_by(subject_id=id).scalar()
    return jsonify({
        "grades": [{"id": g.id, "student_id": g.student_id, "score": g.score} for g in grades],
        "average": avg_score
    })

# GET /subjects/<id>/class-average - overall class average for subject
@subjects_bp.route("/<int:id>/class-average", methods=["GET"])
@jwt_required()
def class_average(id):
    avg_score = db.session.query(func.avg(Grade.score)).filter_by(subject_id=id).scalar()
    if avg_score is None:
        return jsonify({"error": "No grades found for this subject"}), 404
    return jsonify({"subject_id": id, "class_average": round(avg_score, 2)})