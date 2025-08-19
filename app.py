from flask import Flask
from extensions import db, jwt
from config import Config
from routes.students import students_bp
from routes.grades import grades_bp
from routes.subjects import subjects_bp
from routes.auth import auth_bp

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    with app.app_context():
        db.create_all()

    jwt.init_app(app)

    # Register Blueprints
    app.register_blueprint(auth_bp, url_prefix="/auth")
    app.register_blueprint(students_bp, url_prefix="/students")
    app.register_blueprint(grades_bp, url_prefix="/grades")
    app.register_blueprint(subjects_bp, url_prefix="/subjects")

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
