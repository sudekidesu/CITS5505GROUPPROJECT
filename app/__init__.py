from flask import Flask
from app.config import Config
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import CSRFProtect

db = SQLAlchemy()
login = LoginManager()
login.login_view = 'login'
def create_app(config):
    app = Flask(__name__)
    app.config.from_object(config)
    csrf = CSRFProtect(app)
    db.init_app(app)
    login.init_app(app)
    from app.blueprints import main
    app.register_blueprint(main)
    with app.app_context():  # Create an :class:`~flask.ctx.AppContext`.
        db.create_all()

    return app
