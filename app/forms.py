from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, IntegerField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError

from app.models import User


class LoginForm(FlaskForm):
    username = StringField('username', validators=[DataRequired()])
    password = PasswordField('password', validators=[DataRequired()])


# Form：主要就是用来验证前端提交的数据是否符合要求
class RegisterForm(FlaskForm):
    email = StringField(validators=[Email()])
    username = StringField(validators=[Length(min=3, max=20)])
    password = StringField(validators=[Length(min=6, max=20)])
    password_confirm = StringField(validators=[EqualTo("password")])

    # 自定义验证：
    # 1. 邮箱是否已经被注册
    def validate_email(self, field):
        email = field.data
        user = User.query.filter_by(email=email).first()
        if user:
            raise ValidationError(message="该邮箱已经被注册！")


class QuestionForm(FlaskForm):
    title = StringField(validators=[DataRequired()])
    content = StringField([DataRequired()])
    category = StringField([DataRequired()])


class AnswerForm(FlaskForm):
    content = StringField(validators=[DataRequired()])


class CommentForm(FlaskForm):
    content = StringField(validators=[DataRequired()])
    answer_id = IntegerField(validators=[DataRequired()])
    question_id = IntegerField(validators=[DataRequired()])


class PageForm(FlaskForm):
    page = IntegerField(validators=[DataRequired()])
    per_page = IntegerField(validators=[DataRequired()])


class QalikeForm(FlaskForm):
    question_id = IntegerField(validators=[DataRequired()])