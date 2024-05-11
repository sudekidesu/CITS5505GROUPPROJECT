# __init__.py
from flask import Flask
from flask_migrate import Migrate
from flask_wtf import CSRFProtect
from app.exts import init_extensions, db


def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///forumDB.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = 'secret_key'

    csrf = CSRFProtect(app)
    init_extensions(app)

# from app.models import User, Question, Answer, EmailCaptchaModel  # 这里可以根据实际位置调整路径
    with app.app_context():
        db.create_all()

    migrate = Migrate(app, db)

    from app.routes import init_routes
    init_routes(app)

    return app
