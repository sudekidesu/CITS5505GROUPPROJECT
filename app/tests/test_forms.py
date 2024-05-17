import unittest
from app import app, db
from app.forms import LoginForm, RegisterForm, QuestionForm, AnswerForm, CommentForm
from app.models import User

class TestForms(unittest.TestCase):

    def setUp(self):
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        app.config['WTF_CSRF_ENABLED'] = False  # Disable CSRF for testing
        self.app = app.test_client()
        self.app_context = app.app_context()
        self.app_context.push()
        with app.app_context():
            db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_login_form(self):
        with app.test_request_context():
            form = LoginForm(username='testuser', password='password')
            self.assertTrue(form.validate())

    def test_register_form(self):
        with app.test_request_context():
            form = RegisterForm(email='test@example.com', username='testuser', password='password', password_confirm='password')
            self.assertTrue(form.validate())

    def test_register_form_existing_email(self):
        with app.app_context():
            user = User(email='test@example.com', username='existinguser', password='password', password_confirm='password')
            db.session.add(user)
            db.session.commit()

        with app.test_request_context():
            form = RegisterForm(email='test@example.com', username='newuser', password='password', password_confirm='password')
            self.assertFalse(form.validate())

    def test_question_form(self):
        with app.test_request_context():
            form = QuestionForm(title='Question title', content='Question content', category='General')
            self.assertTrue(form.validate())

    def test_answer_form(self):
        with app.test_request_context():
            form = AnswerForm(content='Answer content')
            self.assertTrue(form.validate())

    def test_comment_form(self):
        with app.test_request_context():
            form = CommentForm(content='Comment content', answer_id=1, question_id=1)
            self.assertTrue(form.validate())

if __name__ == '__main__':
    unittest.main()
