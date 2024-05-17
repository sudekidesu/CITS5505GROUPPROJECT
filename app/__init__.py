from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import CSRFProtect

db = SQLAlchemy()
login = LoginManager()
login.login_view = 'login'
def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///forumDB.db'  # 例如 SQLite
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = 'secret_key'
    csrf = CSRFProtect(app)
    db.init_app(app)
    login.init_app(app)
    from app.blueprints import main
    app.register_blueprint(main)
    with app.app_context():  # Create an :class:`~flask.ctx.AppContext`.
        db.create_all()


    return app
