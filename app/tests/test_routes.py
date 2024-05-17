import unittest
from flask import current_app
from app import app, db
from app.models import User


class RouteTestCase(unittest.TestCase):

    def setUp(self):
        self.app = app
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.client = self.app.test_client()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_index_page(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Welcome to the Index Page', response.data)

    def test_user_form_get(self):
        response = self.client.get('/user')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'User Form', response.data)

    def test_user_form_post(self):
        response = self.client.post('/user', data={'name': 'Flask'}, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'User added successfully!', response.data)

        # 检查数据库中是否添加了用户
        user = User.query.filter_by(name='Flask').first()
        self.assertIsNotNone(user)
        self.assertEqual(user.name, 'Flask')

    def test_user_form_post_existing_user(self):
        # 先添加用户
        user = User(name='Flask')
        db.session.add(user)
        db.session.commit()

        response = self.client.post('/user', data={'name': 'Flask'}, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'User already exists.', response.data)


if __name__ == '__main__':
    unittest.main()
