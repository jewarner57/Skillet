from skillet.models import User
from flask_wtf import FlaskForm
from wtforms import StringField, DateField, SelectField, SubmitField, PasswordField
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from wtforms.fields.core import FloatField
from wtforms.validators import DataRequired, Length, URL, ValidationError
from skillet import bcrypt


class SignUpForm(FlaskForm):
    """Form for creating a new user"""
    username = StringField('User Name',
                           validators=[DataRequired(),
                                       Length(min=3, max=50)])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError(
                'That username is taken. Please choose a different one.')


class LoginForm(FlaskForm):
    """Form for logging in a user"""
    username = StringField('User Name',
                           validators=[DataRequired(),
                                       Length(min=3, max=50)])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Log In')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if not user:
            raise ValidationError('No user found with that username.')

    def validate_password(self, password):
        user = User.query.filter_by(username=self.username.data).first()
        if user and not bcrypt.check_password_hash(user.password,
                                                   password.data):
            raise ValidationError('Password does not match.')
