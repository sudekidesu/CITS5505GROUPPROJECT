from flask import redirect, url_for, flash, render_template, request, session, g
from flask_login import current_user, login_user, login_required, LoginManager
import sqlalchemy as sa
from werkzeug.security import generate_password_hash

from app import db
from app import app
from app.forms import LoginForm, RegisterForm, QuestionForm, AnswerForm, CommentForm
from app.models import User, Question, Answer


@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    user = db.session.scalar(
        sa.select(User).where(User.username == form.username.data))
    if user is None or not user.check_password(form.password.data):
        flash('Invalid username or password')
        return redirect(url_for('login'))
    login_user(user)
    return redirect(url_for('index'))


@app.route("/register", methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template("register.html")
    else:
        # 验证用户提交的邮箱和验证码是否对应且正确
        # 表单验证：flask-wtf: wtforms
        form = RegisterForm(request.form)
        email = form.email.data
        username = form.username.data
        password = form.password.data
        user = User(email=email, username=username, password_hash=generate_password_hash(password))
        db.session.add(user)
        db.session.commit()
        return redirect(url_for("login"))


@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")


@app.route("/qa/public", methods=['GET', 'POST'])
@login_required
def public_question():
    if request.method == 'GET':
        return render_template("public_question.html")
    else:
        form = QuestionForm(request.form)
        if form.validate():
            title = form.title.data
            content = form.content.data
            question = Question(title=title, content=content, author=g.user)
            db.session.add(question)
            db.session.commit()
            # todo: 跳转到这篇问答的详情页
            return redirect("/")
        else:
            print(form.errors)
            return redirect(url_for("qa.public_question"))


@app.route("/qa/detail/<qa_id>")
def qa_detail(qa_id):
    question = Question.query.get(qa_id)
    return render_template("detail.html", question=question)

@app.post("/answer/public")
@login_required
def public_answer():
    form = AnswerForm(request.form)
    if form.validate():
        content = form.content.data
        question_id = form.question_id.data
        answer = Answer(content=content, question_id=question_id, author_id=g.user.id)
        db.session.add(answer)
        db.session.commit()
        return redirect(url_for("qa.qa_detail", qa_id=question_id))
    else:
        print(form.errors)
        return redirect(url_for("qa.qa_detail", qa_id=request.form.get("question_id")))


@app.route("/search")
def search():
    # /search?q=flask
    # /search/<q>
    # post, request.form
    q = request.args.get("q")
    questions = Question.query.filter(Question.title.contains(q)).all()
    return render_template("index.html", questions=questions)


@app.post("/comment/public")
@login_required
def public_comment():
    form = CommentForm(request.form)
    if form.validate():
        content = form.content.data
        score = form.score.data
        answer_id = form.answer_id.data
        comment = Answer(content=content, answer_id=answer_id, score=score, author_id=g.user.id)
        db.session.add(comment)
        db.session.commit()
        return redirect(url_for("qa.ans_detail", ans_id=answer_id))
    else:
        print(form.errors)
        return redirect(url_for("qa.ans_detail", ans_id=request.form.get("answer_id")))
