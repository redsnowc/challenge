from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import Length, Email, EqualTo, DataRequired, AnyOf
from simpledu.models import db, User, Course, Live
from wtforms import ValidationError
from wtforms import TextAreaField, IntegerField
from wtforms.validators import URL, NumberRange


class RegisterForm(FlaskForm):
    username = StringField(
            '用户名', validators=[DataRequired(), Length(3, 24)])
    email = StringField('邮箱', validators=[DataRequired(), Email()])
    password = PasswordField(
            '密码', validators=[DataRequired(), Length(6, 24)])
    repeat_password = PasswordField(
            '重复密码', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('提交')

    def create_user(self):
        user = User()
        user.username = self.username.data
        user.email = self.email.data
        user.password = self.password.data
        db.session.add(user)
        db.session.commit()
        return user
    
    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('用户名已存在')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('邮箱已存在')

class LoginForm(FlaskForm):
    email = StringField('邮箱', validators=[DataRequired(), Email()])
    password = PasswordField(
            '密码', validators=[DataRequired(), Length(6, 24)])
    remember_me = BooleanField('记住我')
    submit = SubmitField('提交')

    def validate_email(self, field):
        if not User.query.filter_by(email=field.data).first():
            raise ValidationError('邮箱未注册')

    def validate_password(self, field):
        user = User.query.filter_by(email=self.email.data).first()
        if user and not user.check_password(field.data):
            raise ValidationError('密码错误')

class CourseForm(FlaskForm):
    name = StringField('课程名称', validators=[DataRequired(), Length(5,32)])
    description = TextAreaField(
            '课程简介', validators=[DataRequired(), Length(20, 256)])
    image_url = StringField('封面图片', validators=[DataRequired(), URL()])
    author_id = IntegerField('作者ID', validators=[DataRequired(),NumberRange(min=1, message='无效的用户ID')])
    submit = SubmitField('提交')

    def validate_author_id(self, field):
        if not User.query.get(field.data):
            raise ValidationError('用户不存在')

    def create_course(self):
        course = Course()
        self.populate_obj(course)
        db.session.add(course)
        db.session.commit()
        return course

    def update_course(self, course):
        self.populate_obj(course)
        db.session.add(course)
        db.session.commit()
        return course

class UserForm(RegisterForm):
    role = IntegerField('用户权限', validators=[DataRequired(),AnyOf([10, 20, 30], message='无的效用户权限')])
    submit = SubmitField('提交')

    def create_user(self):
        user = User()
        self.populate_obj(user)
        db.session.add(user)
        db.session.commit()
        return user

class EditUserForm(FlaskForm):
    username = StringField(
            '用户名', validators=[DataRequired(), Length(3, 24)])
    email = StringField('邮箱', validators=[DataRequired(), Email()])
    password = PasswordField(
            '密码', validators=[DataRequired(), Length(6, 24)])
    repeat_password = PasswordField(
            '重复密码', validators=[DataRequired(), EqualTo('password')])
    role = IntegerField('用户权限', validators=[DataRequired(),AnyOf([10, 20, 30], message='无效的用户权限')])    
    submit = SubmitField('提交')
    
    def update_user(self, user):
        self.populate_obj(user)
        db.session.add(user)
        db.session.commit()
        return user

class CreateLive(FlaskForm):
    name = StringField(
            '直播名称', validators=[DataRequired(), Length(5,32)])
    user_id = IntegerField('用户ID', validators=[DataRequired(),NumberRange(min=1, message='无效的用户ID')])
    live_url = StringField('直播地址', validators=[DataRequired(), URL()])
    submit = SubmitField('提交')

    def validate_user_id(self, field): 
        if not User.query.get(field.data):
            raise ValidationError('用户不存在')

    def create_live(self):
        live = Live()
        self.populate_obj(live)
        db.session.add(live)
        db.session.commit()
        return live
        
