from flask import redirect, url_for, flash, render_template, request, session, g, jsonify
from flask_login import current_user, login_user, login_required
from flask_wtf.csrf import generate_csrf

from app.blueprints import main
from app.controllers import UserController, QuestionController, AnswerController
from app.forms import LoginForm, RegisterForm, QuestionForm, AnswerForm, QalikeForm

user_controller = UserController()
question_controller = QuestionController()
answer_controller = AnswerController()

@main.route('/csrf-token')
def csrf_token():
    token = generate_csrf()
    return jsonify({'csrfToken': token})

@main.route('/shutdown', methods=['GET'])
def shutdown():
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    func()
    return 'Server shutting down...'

@main.route('/', methods=['GET', 'POST'])
def index():
    if current_user.is_authenticated:
        return render_template('index.html', user=g._login_user)
    else:
        print("index")
        token = generate_csrf()
        return render_template('index.html', token=token)


@main.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    if request.method == 'GET':
        token = generate_csrf()
        print(token)
        return render_template("login.html", token=token)
    else:
        form = LoginForm(request.form)
        if form.validate():
            user, msg = user_controller.get_user_by_name(form.username.data)
            if user is None or not user.check_password(form.password.data):
                flash('Invalid username or password')
                return redirect(url_for('main.login'))

            login_user(user)
            return redirect(url_for('main.index'))
        else:
            return redirect(url_for("main.login"))


@main.route("/register", methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        token = generate_csrf()
        return render_template("register.html", token=token)
    else:
        # 验证用户提交的邮箱和验证码是否对应且正确
        # 表单验证：flask-wtf: wtforms
        form = RegisterForm(request.form)
        print("validate: " + str(form.validate()))
        if form.validate():
            email = form.email.data
            username = form.username.data
            password = form.password.data
            msg = user_controller.add_user(email, username, password)
            return redirect(url_for("main.login"))
        else:
            return redirect(url_for("main.register"))


@main.route("/logout")
def logout():
    session.clear()
    return redirect("/")


@main.route("/qa/public", methods=['GET', 'POST'])
@login_required
def public_question():
    if request.method == 'GET':
        token = generate_csrf()
        return render_template("ask_question.html", token=token, user=current_user)
    else:
        form = QuestionForm(request.form)
        if form.validate():
            title = form.title.data
            category = form.category.data
            content = form.content.data
            qa_id, msg = question_controller.add_question(title, category, content, current_user)
            return redirect(url_for("main.qa_detail", qa_id=qa_id))
        else:
            print(form.errors)
            return redirect(url_for("main.public_question"))


@main.route("/qa/detail/<qa_id>", methods=['GET', 'POST'])
def qa_detail(qa_id):
    if request.method == 'GET':
        question, msg = question_controller.get_question_by_id(qa_id)
        question_data = {"id": question.id,
                       "authorid": question.author_id,
                       "username": question.author.username,
                       "category": question.category,
                       "title": question.title,
                       "content": question.content,
                       "create_time": question.create_time,
                       "likes": question.likes
                       }
        token = generate_csrf()
        page = request.args.get("page", default=1, type=int)
        per_page = request.args.get("per_page", default=10, type=int)
        pagination, msg = answer_controller.get_answer_by_qaid(question.id, page, per_page)
        answers = pagination.items
        answers_data = [{"id": answer.id,
                       "author": answer.author_id,
                       "username": answer.author.username,
                       "content": answer.content,
                       "create_time": answer.create_time
                       } for answer in answers]
        return render_template("post-details.html", question_data=question_data, token=token, answers_data=answers_data, user=current_user)
    else:
        if not current_user.is_authenticated:
            return redirect(url_for('main.qa_detail', qa_id=qa_id))
        form = AnswerForm(request.form)
        if form.validate():
            question_id = qa_id
            content = form.content.data
            answer, msg = answer_controller.add_answer(question_id, content, current_user)
            msg = question_controller.update_answer_time(qa_id, answer.create_time)
            return redirect(url_for("main.qa_detail", qa_id=qa_id))
        else:
            print(form.errors)
            return redirect(url_for("main.qa_detail", qa_id=qa_id))


# @main.post("/answer/public")
# @login_required
# def public_answer():
#     form = AnswerForm(request.form)
#     if form.validate():
#         content = form.content.data
#         question_id = form.question_id.data
#         answer = Answer(content=content, question_id=question_id, author_id=g._login_user.id)
#         db.session.add(answer)
#         db.session.commit()
#         return redirect(url_for("main.qa_detail", qa_id=question_id))
#     else:
#         print(form.errors)
#         return redirect(url_for("main.qa_detail", qa_id=request.form.get("question_id")))


# @main.post("/comment/public")
# @login_required
# def public_comment():
#     form = CommentForm(request.form)
#     if form.validate():
#         question_id = form.question_id.data
#         content = form.content.data
#         answer_id = form.answer_id.data
#         comment = Answer(content=content, answer_id=answer_id, author_id=g._login_user.id)
#         db.session.add(comment)
#         db.session.commit()
#         return redirect(url_for("main.qa_detail", qa_id=question_id,user=current_user))
#     else:
#         print(form.errors)
#         return redirect(url_for("main.qa_detail", qa_id=request.form.get("question_id"),user=current_user))


@main.route("/search")
def search():
    # /search?q=flask
    # /search/<q>
    # post, request.form
    q = request.args.get("q")
    page = request.args.get("page", default=1, type=int)
    per_page = request.args.get("per_page", default=10, type=int)
    pagination, msg = question_controller.search_question_by_title(q, page, per_page)
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


@main.route("/qa/like", methods=['POST'])
@login_required
def like():
    form = QalikeForm(request.form)
    if form.validate():
        question_id = form.question_id.data
        question_likes, author_id, msg = question_controller.like(question_id)
        if author_id:
            likes, user_id, msg = user_controller.like(author_id)
            return jsonify({'message': 'Like added', 'total_likes': question_likes}), 200
        else:
            return jsonify({'message': 'Question not found'}), 404
    else:
        return jsonify({'message': 'Missing \'qa_id\''}), 404


# @main.route("/qa/dislike/<qa_id>", methods=['POST'])
# def dislike(qa_id):
#     question = Question.query.get(qa_id)
#     if question:
#         auth_id = question.author_id
#         author = User.query.get(auth_id)
#         if question.likes > 0:
#             question.likes += 1
#         if author.likes > 0:
#             author.likes += 1
#         db.session.commit()
#         return jsonify({'message': 'Disliked', 'total_likes': question.likes}), 200
#     else:
#         return jsonify({'message': 'Question not found'}), 404


@main.route("/board")
def board():
    page = request.args.get("page", default=1, type=int)
    per_page = request.args.get("per_page", default=5, type=int)
    pagination, msg = user_controller.get_comunity_board(page, per_page)
    users = pagination.items
    users_data = [{"id": user.id,
                   "username": user.username,
                   "likes": user.likes
                   } for user in users]
    response = {
        "questions": users_data,
        "total": pagination.total,
        "pages": pagination.pages,
        "current_page": pagination.page
    }
    return jsonify(response)

@main.route("/recentqa")
def recentqa():
    page = request.args.get("page", default=1, type=int)
    per_page = request.args.get("per_page", default=10, type=int)
    pagination, msg = question_controller.get_recent_questions(page, per_page)
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


@main.route("/recentanswered")
def recentanswered():
    page = request.args.get("page", default=1, type=int)
    per_page = request.args.get("per_page", default=10, type=int)
    pagination, msg = question_controller.get_recent_answered(page, per_page)
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


@main.route("/about")
def about():
    if current_user.is_authenticated:
        return render_template('About_us.html',user=current_user)
    else:
        token = generate_csrf()
        return render_template('About_us.html',user=None)