from skillet.models import User
from flask_wtf import FlaskForm
from wtforms import StringField, DateField, SelectField, SubmitField, PasswordField
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from wtforms.fields.core import FloatField
from wtforms.validators import DataRequired, Length, URL, ValidationError, Email
from skillet import bcrypt


class SignUpForm(FlaskForm):
    """Form for creating a new user"""
    email = StringField('Email',
                        validators=[DataRequired(),
                                    Length(min=3, max=50), Email()])
    username = StringField('User Name',
                           validators=[DataRequired(),
                                       Length(min=3, max=50)])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Sign Up')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError(
                'That email is already associated with another account.')


class LoginForm(FlaskForm):
    """Form for logging in a user"""
    email = StringField('Email',
                        validators=[DataRequired(),
                                    Length(min=3, max=50), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Log In')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if not user:
            raise ValidationError('No user found with that email.')

    def validate_password(self, password):
        user = User.query.filter_by(email=self.email.data).first()
        if user and not bcrypt.check_password_hash(user.password,
                                                   password.data):
            raise ValidationError('Invalid Username or Password')
