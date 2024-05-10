from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///forumDB.db'  # 例如 SQLite
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'secret_key'
db = SQLAlchemy(app)
from app import models

with app.app_context():  # Create an :class:`~flask.ctx.AppContext`.
    db.create_all()

migrate = Migrate(app, db)

from app import routes
