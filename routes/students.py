from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from models.student import Student
from extensions import db
from models.grade import Grade
from models.subject import Subject
from sqlalchemy import func

students_bp = Blueprint("students", __name__)

# POST /students - Add new student
@students_bp.route("", methods=["POST"])
@jwt_required()
def add_student():
    data = request.json
    if Student.query.filter_by(email=data.get("email")).first():
        return jsonify({"error": "Student already exists"}), 400
    student = Student(name=data.get("name"), email=data.get("email"))
    db.session.add(student)
    db.session.commit()
    return jsonify({"message": "Student added successfully"})

# GET /students - List students
@students_bp.route("", methods=["GET"])
@jwt_required()
def list_students():
    students = Student.query.all()
    return jsonify([{"id": s.id, "name": s.name, "email": s.email} for s in students])

# GET /students/<id>/average - student overall average
@students_bp.route("/<int:id>/average", methods=["GET"])
@jwt_required()
def student_average(id):
    avg_score = db.session.query(func.avg(Grade.score)).filter_by(student_id=id).scalar()
    if avg_score is None:
        return jsonify({"error": "No grades found for this student"}), 404
    return jsonify({"student_id": id, "average": round(avg_score, 2)})

# GET /students/<id>/report-card - full report card
@students_bp.route("/<int:id>/report-card", methods=["GET"])
@jwt_required()
def report_card(id):
    grades = (
        db.session.query(Subject.name, Grade.score)
        .join(Subject, Grade.subject_id == Subject.id)
        .filter(Grade.student_id == id)
        .all()
    )
    if not grades:
        return jsonify({"error": "No grades found for this student"}), 404

    avg_score = db.session.query(func.avg(Grade.score)).filter_by(student_id=id).scalar()

    return jsonify({
        "student_id": id,
        "grades": [{"subject": g[0], "score": g[1]} for g in grades],
        "overall_average": round(avg_score, 2)
    })
