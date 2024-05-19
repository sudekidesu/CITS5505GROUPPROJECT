from sqlalchemy import desc
from werkzeug.security import generate_password_hash

from app import db
from app.models import User, Question, Answer

import sqlalchemy as sa


class UserController:
    def get_user_by_id(self, id):
        try:
            user = db.session.scalar(sa.select(User).where(User.id == id))
            return user, '200'
        except Exception as e:
            return None, '500'

    def get_user_by_name(self, username):
        try:
            user = db.session.scalar(sa.select(User).where(User.username == username))
            return user, '200'
        except Exception as e:
            return None, '500'

    def add_user(self, email, username, password):
        try:
            user = User(email=email, username=username, password_hash=generate_password_hash(password))
            db.session.add(user)
            db.session.commit()
            return '200'
        except Exception as e:
            return '500'

    def like(self, id):
        try:
            user = db.session.scalar(sa.select(User).where(User.id == id))
            if user is None:
                return None, None, '404'  # User not found
            user.likes += 1
            db.session.commit()
            return user.likes, user.id, '200'
        except Exception as e:
            return None, None, '500'

    def get_comunity_board(self, page, per_page):
        try:
            pagination = User.query.order_by(desc(User.likes)).paginate(page=page, per_page=per_page)
            return pagination, '200'
        except Exception as e:
            return None, '500'


class QuestionController:
    def add_question(self, title, category, content, author):
        try:
            question = Question(title=title, category=category, content=content, author=author)
            db.session.add(question)
            db.session.commit()
            return question.id, '200'
        except Exception as e:
            return None, '500'

    def get_question_by_id(self, qa_id):
        try:
            question = Question.query.get(qa_id)
            return question, '200'
        except Exception as e:
            return None, '500'

    def update_answer_time(self, qa_id, update_time):
        try:
            question = Question.query.get(qa_id)
            question.update_time = update_time
            db.session.commit()
            return '200'
        except Exception as e:
            return '500'

    def search_question_by_title(self, str, page, per_page):
        try:
            pagination  = Question.query.filter(Question.title.contains(str)).order_by(desc(Question.create_time)).paginate(page=page, per_page=per_page)
            return pagination, '200'
        except Exception as e:
            return None, '500'

    def like(self, id):
        try:
            question, msg = self.get_question_by_id(id)
            question.likes += 1
            db.session.commit()
            return question.likes, question.author_id, '200'
        except Exception as e:
            return None, None, '500'

    def get_recent_questions(self, page, per_page):
        try:
            pagination = Question.query.order_by(desc(Question.create_time)).paginate(page=page, per_page=per_page)
            return pagination, '200'
        except Exception as e:
            return None, '500'

    def get_recent_answered(self, page, per_page):
        try:
            pagination  = Question.query.order_by(desc(Question.update_time)).paginate(page=page, per_page=per_page)
            return pagination, '200'
        except Exception as e:
            return None, '500'




class AnswerController:
    def add_answer(self, question_id, content, author):
        try:
            answer = Answer(content=content, question_id=question_id, author=author)
            db.session.add(answer)
            db.session.commit()
            return answer, '200'
        except Exception as e:
            return None, '500'

    def get_answer_by_qaid(self, qa_id, page, per_page):
        try:
            pagination = Answer.query.filter(Answer.question_id == qa_id).order_by().paginate(page=page,
                                                                                              per_page=per_page)
            return pagination, '200'
        except Exception as e:
            return None, '500'
