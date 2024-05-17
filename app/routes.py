from flask import redirect, url_for, flash, render_template, request, session, g, jsonify
from flask_login import current_user, login_user, login_required, LoginManager
import sqlalchemy as sa
from flask_wtf.csrf import generate_csrf
from sqlalchemy import desc
from werkzeug.security import generate_password_hash

from app import db
from app import app
from app.forms import LoginForm, RegisterForm, QuestionForm, AnswerForm, CommentForm, PageForm, QalikeForm
from app.models import User, Question, Answer


@app.route('/csrf-token')
def csrf_token():
    token = generate_csrf()
    return jsonify({'csrfToken': token})


@app.route('/', methods=['GET', 'POST'])
def index():
    if current_user.is_authenticated:
        return render_template('index.html', user=g._login_user)
    else:
        token = generate_csrf()
        return render_template('index.html', token=token)
    

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    if request.method == 'GET':
        token = generate_csrf()
        print(token)
        return render_template("login.html", token=token)
    else:
        form = LoginForm(request.form)
        if form.validate():
            user = db.session.scalar(
                sa.select(User).where(User.username == form.username.data))
            if user is None or not user.check_password(form.password.data):
                flash('Invalid username or password')
                return redirect(url_for('login'))
            # login_user(user, remember=True)
            login_user(user) # , remember=False)
            return redirect(url_for('index'))
        else:
            return redirect(url_for("login"))


@app.route("/register", methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        token = generate_csrf()
        return render_template("register.html", token=token)
    else:
        # 验证用户提交的邮箱和验证码是否对应且正确
        # 表单验证：flask-wtf: wtforms
        print(request)
        form = RegisterForm(request.form)
        if form.validate():
            email = form.email.data
            username = form.username.data
            password = form.password.data
            user = User(email=email, username=username, password_hash=generate_password_hash(password))
            db.session.add(user)
            db.session.commit()
            return redirect(url_for("login"))
        else:
            return redirect(url_for("register"))


@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")


@app.route("/qa/public", methods=['GET', 'POST'])
@login_required
def public_question():
    if request.method == 'GET':
        token = generate_csrf()
        return render_template("ask_question.html", token=token, user=g._login_user)
    else:
        form = QuestionForm(request.form)
        if form.validate():
            title = form.title.data
            category = form.category.data
            content = form.content.data
            question = Question(title=title, category=category, content=content, author=current_user)
            db.session.add(question)
            db.session.commit()
            return redirect(url_for("qa_detail", qa_id=question.id))
        else:
            print(form.errors)
            return redirect(url_for("public_question"))


@app.route("/qa/detail/<qa_id>", methods=['GET', 'POST'])
def qa_detail(qa_id):
    if request.method == 'GET':
        # qa_id = request.args.get("question_id")
        question = Question.query.get(qa_id)
        question_data = {"id": question.id,
                       "authorid": question.author_id,
                       "username": question.author.username,
                       "category": question.category,
                       "content": question.content,
                       "create_time": question.create_time,
                       "likes": question.likes
                       }
        token = generate_csrf()
        page = request.args.get("page", default=1, type=int)
        per_page = request.args.get("per_page", default=10, type=int)
        pagination = Answer.query.filter(Answer.question_id==qa_id).order_by().paginate(page=page, per_page=per_page)
        answers = pagination.items
        answers_data = [{"id": answer.id,
                       "author": answer.author_id,
                       "username": answer.author.username,
                       "content": answer.content,
                       "create_time": answer.create_time
                       } for answer in answers]
        return render_template("question.html", question_data=question_data, token=token, answers_data=answers_data)
    else:
        if not current_user.is_authenticated:
            return redirect(url_for('qa_detail', qa_id=qa_id))
        form = AnswerForm(request.form)
        if form.validate():
            question_id = qa_id
            content = form.content.data
            answer = Answer(content=content, question_id=question_id, author=current_user)
            db.session.add(answer)
            question = Question.query.get(qa_id)
            question.update_time = answer.create_time
            db.session.commit()
            return redirect(url_for("qa_detail", qa_id=qa_id))
        else:
            print(form.errors)
            return redirect(url_for("qa_detail", qa_id=qa_id))



@app.post("/answer/public")
@login_required
def public_answer():
    form = AnswerForm(request.form)
    if form.validate():
        content = form.content.data
        question_id = form.question_id.data
        answer = Answer(content=content, question_id=question_id, author_id=g._login_user.id)
        db.session.add(answer)
        db.session.commit()
        return redirect(url_for("qa_detail", qa_id=question_id))
    else:
        print(form.errors)
        return redirect(url_for("qa_detail", qa_id=request.form.get("question_id")))


@app.post("/comment/public")
@login_required
def public_comment():
    form = CommentForm(request.form)
    if form.validate():
        question_id = form.question_id.data
        content = form.content.data
        answer_id = form.answer_id.data
        comment = Answer(content=content, answer_id=answer_id, author_id=g._login_user.id)
        db.session.add(comment)
        db.session.commit()
        return redirect(url_for("qa_detail", qa_id=question_id))
    else:
        print(form.errors)
        return redirect(url_for("qa_detail", qa_id=request.form.get("question_id")))


@app.route("/search")
def search():
    # /search?q=flask
    # /search/<q>
    # post, request.form
    q = request.args.get("q")
    page = request.args.get("page", default=1, type=int)
    per_page = request.args.get("per_page", default=10, type=int)
    pagination  = Question.query.filter(Question.title.contains(q)).order_by(desc(Question.create_time)).paginate(page=page, per_page=per_page)
    questions = pagination.items
    questions_data = [{"id": question.id,
                       "author": question.author_id,
                       "username": question.author.username,
                       "title": question.title,
                       "category": question.category,
                       "content": question.content,
                       "create_time": question.create_time,
                       "likes": question.likes
                       } for question in questions]

    response = {
        "questions": questions_data,
        "total": pagination.total,
        "pages": pagination.pages,
        "current_page": pagination.page
    }
    return jsonify(response)


@app.route("/recentqa")
def recentqa():
    page = request.args.get("page", default=1, type=int)
    per_page = request.args.get("per_page", default=10, type=int)
    pagination  = Question.query.order_by(desc(Question.create_time)).paginate(page=page, per_page=per_page)
    questions = pagination.items
    questions_data = [{"id": question.id,
                       "author": question.author_id,
                       "username": question.author.username,
                       "title": question.title,
                       "category": question.category,
                       "content": question.content,
                       "create_time": question.create_time,
                       "likes": question.likes
                       } for question in questions]

    response = {
        "questions": questions_data,
        "total": pagination.total,
        "pages": pagination.pages,
        "current_page": pagination.page
    }
    return jsonify(response)


@app.route("/qa/like", methods=['POST'])
@login_required
def like():
    form = QalikeForm(request.form)
    if form.validate():
        question_id = form.question_id.data
        question = Question.query.get(question_id)
        if question:
            auth_id = question.author_id
            author = User.query.get(auth_id)
            question.likes += 1
            author.likes += 1
            db.session.commit()
            return jsonify({'message': 'Like added', 'total_likes': question.likes}), 200
        else:
            return jsonify({'message': 'Question not found'}), 404
    else:
        return jsonify({'message': 'Missing \'qa_id\''}), 404


@app.route("/qa/dislike/<qa_id>", methods=['POST'])
def dislike(qa_id):
    question = Question.query.get(qa_id)
    if question:
        auth_id = question.author_id
        author = User.query.get(auth_id)
        if question.likes > 0:
            question.likes += 1
        if author.likes > 0:
            author.likes += 1
        db.session.commit()
        return jsonify({'message': 'Disliked', 'total_likes': question.likes}), 200
    else:
        return jsonify({'message': 'Question not found'}), 404


@app.route("/board")
def board():

    page = request.args.get("page", default=1, type=int)
    per_page = request.args.get("per_page", default=5, type=int)
    pagination = User.query.order_by(desc(User.likes)).paginate(page=page, per_page=per_page)
    users_data = [{"id": user.id,
                   "username": user.username,
                   "likes": user.likes
                   } for user in pagination]
    response = {
        "questions": users_data,
        "total": pagination.total,
        "pages": pagination.pages,
        "current_page": pagination.page
    }
    return jsonify(response)

@app.route("/recentanswered")
def recentanswered():
    page = request.args.get("page", default=1, type=int)
    per_page = request.args.get("per_page", default=10, type=int)
    pagination  = Question.query.order_by(desc(Question.update_time)).paginate(page=page, per_page=per_page)
    questions = pagination.items
    questions_data = [{"id": question.id,
                       "author": question.author_id,
                       "username": question.author.username,
                       "title": question.title,
                       "category": question.category,
                       "content": question.content,
                       "create_time": question.create_time,
                       "update_time": question.update_time,
                       "likes": question.likes
                       } for question in questions]

    response = {
        "questions": questions_data,
        "total": pagination.total,
        "pages": pagination.pages,
        "current_page": pagination.page
    }
    return jsonify(response)

@app.route("/about")
def about():
    return render_template('About_us.html')