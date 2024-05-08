from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, IntegerField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError

from app.models import User


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')


# Form：主要就是用来验证前端提交的数据是否符合要求
class RegisterForm(FlaskForm):
    email = StringField(validators=[Email()])
    captcha = StringField(validators=[Length(min=4, max=4)])
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


class AnswerForm(FlaskForm):
    content = StringField(validators=[DataRequired()])
    question_id = IntegerField(validators=[DataRequired()])


class CommentForm(FlaskForm):
    content = StringField(validators=[DataRequired()])
    score = IntegerField(validators=[DataRequired()])
    answer_id = IntegerField(validators=[DataRequired()])
