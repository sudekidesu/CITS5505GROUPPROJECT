# routes.py
from flask import Blueprint, current_app, redirect, url_for, flash, render_template, request, session, jsonify
from flask_login import current_user, login_user, login_required
from sqlalchemy import select
from app.exts import db
from app.forms import LoginForm, RegisterForm, QuestionForm, AnswerForm, CommentForm
from app.models import User, EmailCaptchaModel

bp = Blueprint('main', __name__)

@bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = db.session.scalar(select(User).where(User.username == form.username.data))
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect(url_for('main.index'))
        flash('Invalid username or password')
    return render_template('login.html', form=form)

@bp.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('main.login'))
    return render_template('register.html', form=form)

@bp.route('/')
def index():
    return render_template('index.html')

def init_routes(app):
    app.register_blueprint(bp)

# 根据实际需要添加其他路由。
