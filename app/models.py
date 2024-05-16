from datetime import datetime
from flask_login import UserMixin
from flask_login import LoginManager

from app import db, app
from werkzeug.security import generate_password_hash
from werkzeug.security import check_password_hash
# from app import login

login = LoginManager(app)

class User(UserMixin, db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    likes = db.Column(db.Integer, default=0)

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


@login.user_loader
def load_user(id):
    return db.session.get(User, int(id))


class Question(db.Model):
    __tablename__ = "question"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(100), nullable=False)
    category = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    create_time = db.Column(db.DateTime, default=datetime.now)
    likes = db.Column(db.Integer, default=0)

    # 外键
    author_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    author = db.relationship(User, backref="questions")


class Answer(db.Model):
    __tablename__ = "answer"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    content = db.Column(db.Text, nullable=False)
    create_time = db.Column(db.DateTime, default=datetime.now)

    # 外键
    question_id = db.Column(db.Integer, db.ForeignKey("question.id"))
    author_id = db.Column(db.Integer, db.ForeignKey("user.id"))

    # 关系
    question = db.relationship(Question, backref=db.backref("answers", order_by=create_time.desc()))
    author = db.relationship(User, backref="answers")


class Comment(db.Model):
    __tablename__ = "comment"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    content = db.Column(db.Text, nullable=False)
    score = db.Column(db.Integer)
    create_time = db.Column(db.DateTime, default=datetime.now)

    # 外键
    answer_id = db.Column(db.Integer, db.ForeignKey("answer.id"))
    author_id = db.Column(db.Integer, db.ForeignKey("user.id"))

    # # 关系
    answer = db.relationship(Answer, backref=db.backref("comments", order_by=create_time.desc()))
    author = db.relationship(User, backref="comments")
