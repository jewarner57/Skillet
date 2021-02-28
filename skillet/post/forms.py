from skillet.models import Meal, Recipe, User
from flask_wtf import FlaskForm
from wtforms import StringField, DateField, SelectField, SubmitField
from wtforms.ext.sqlalchemy.fields import (
    QuerySelectField, QuerySelectMultipleField)
from wtforms.fields.simple import TextAreaField
from wtforms.fields.core import FloatField
from wtforms.validators import DataRequired, Length, URL, ValidationError
from skillet import bcrypt
from datetime import datetime


class MealForm(FlaskForm):
    """Form for creating a new meal"""
    name = StringField('Name', validators=[Length(min=3, max=50)])
    image_url = StringField('Image Url', validators=[DataRequired(), URL()])
    description = StringField('Description', validators=[DataRequired()])
    recipes = QuerySelectMultipleField(
        'Recipe', query_factory=lambda: Recipe.query)

    submit = SubmitField('Submit')


class RecipeForm(FlaskForm):
    """Form for creating a new recipe"""
    name = StringField('Name', validators=[Length(min=3, max=50)])

    description = TextAreaField(
        'Description', validators=[DataRequired(), Length(min=1, max=300)])

    instructions = TextAreaField(
        'Instructions', validators=[DataRequired(), Length(min=30, max=300)])

    ingredients = TextAreaField(
        'Ingredients', validators=[DataRequired(), Length(min=30, max=300)])

    submit = SubmitField('Submit')
