import unittest
from unittest.mock import patch, MagicMock
from app import create_app, db
from app.config import TestConfig
from app.controllers import UserController
from app.models import User


class TestController(unittest.TestCase):

    def setUp(self):
        testApp = create_app(TestConfig)
        self.app_context = testApp.app_context()
        self.app_context.push()
        db.create_all()
        self.controller = UserController()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    @patch('app.db.session.scalar')
    def test_get_user_by_name(self, mock_scalar):
        mock_user = MagicMock(spec=User)
        mock_scalar.return_value = mock_user
        user, status = self.controller.get_user_by_name('testuser')
        self.assertEqual(status, '200')
        self.assertEqual(user, mock_user)

    @patch('app.db.session.scalar')
    def test_get_user_by_id(self, mock_scalar):
        mock_user = MagicMock(spec=User)
        mock_scalar.return_value = mock_user
        user, status = self.controller.get_user_by_id(1)
        self.assertEqual(status, '200')
        self.assertEqual(user, mock_user)

    @patch('app.db.session.add')
    @patch('app.db.session.commit')
    def test_add_user(self, mock_commit, mock_add):
        with patch('werkzeug.security.generate_password_hash', return_value='hashedpassword'):
            status = self.controller.add_user('test@example.com', 'testuser', 'password')
            self.assertEqual(status, '200')
            mock_add.assert_called_once()
            mock_commit.assert_called_once()

    @patch('app.db.session.commit')
    @patch('app.db.session.scalar')
    def test_like_user_exists(self, mock_scalar, mock_commit):
        mock_user = MagicMock(spec=User)
        mock_user.id = 1
        mock_user.likes = 0
        mock_scalar.return_value = mock_user
        likes, user_id, status = self.controller.like(1)
        self.assertEqual(status, '200')
        self.assertEqual(likes, 1)
        self.assertEqual(user_id, 1)
        self.assertEqual(mock_user.likes, 1)
        mock_commit.assert_called_once()

    @patch('app.db.session.commit')
    @patch('app.db.session.scalar')
    def test_like_user_not_exists(self, mock_scalar, mock_commit):
        mock_scalar.return_value = None

        likes, id, status = self.controller.like(1)

        self.assertEqual(status, '404')
        self.assertIsNone(likes)
        self.assertIsNone(id)
        mock_commit.assert_not_called()

    @patch('app.models.User.query')
    def test_get_comunity_board_success(self, mock_query):
        mock_pagination = MagicMock()
        mock_query.order_by.return_value.paginate.return_value = mock_pagination
        pagination, status = self.controller.get_comunity_board(1, 10)
        self.assertEqual(status, '200')
        self.assertIs(pagination, mock_pagination)

    @patch('app.models.User.query')
    def test_get_comunity_board_exception(self, mock_query):
        mock_query.order_by.side_effect = Exception("Database error")
        pagination, status = self.controller.get_comunity_board(1, 10)
        self.assertEqual(status, '500')
        self.assertIsNone(pagination)

