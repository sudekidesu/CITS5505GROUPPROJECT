from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, IntegerField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError

# 将模型的导入移到需要时进行
def get_models():
    from app.models import User, EmailCaptchaModel
    return User, EmailCaptchaModel

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])

class RegisterForm(FlaskForm):
    email = StringField('Email', validators=[Email()])
    username = StringField('Username', validators=[Length(min=3, max=20)])
    password = StringField('Password', validators=[Length(min=6, max=20)])
    password_confirm = StringField('Confirm Password', validators=[EqualTo('password')])

    def validate_email(self, field):
        User, EmailCaptchaModel = get_models()
        user = User.query.filter_by(email=field.data).first()
        if user:
            raise ValidationError("该邮箱已经被注册！")

    def validate_captcha(self, field):
        User, EmailCaptchaModel = get_models()
        captcha = field.data
        email = self.email.data
        captcha_model = EmailCaptchaModel.query.filter_by(email=email, captcha=captcha).first()
        if not captcha_model:
            raise ValidationError("邮箱或验证码错误！")

class QuestionForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    content = StringField('Content', validators=[DataRequired()])

class AnswerForm(FlaskForm):
    content = StringField('Content', validators=[DataRequired()])
    question_id = IntegerField('Question ID', validators=[DataRequired()])

class CommentForm(FlaskForm):
    content = StringField('Content', validators=[DataRequired()])
    score = IntegerField('Score', validators=[DataRequired()])
    answer_id = IntegerField('Answer ID', validators=[DataRequired()])
