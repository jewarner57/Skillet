from enum import unique
from sqlalchemy_utils import URLType
from flask_login import UserMixin
from skillet import db


class User(UserMixin, db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(80), nullable=False, unique=True)
    username = db.Column(db.String(80), nullable=False)
    password = db.Column(db.String(200), nullable=False)

    date_created = db.Column(db.DateTime, nullable=False)
    last_logged_in = db.Column(db.DateTime, nullable=False)


class Meal(db.Model):
    __tablename__ = 'meal'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    description = db.Column(db.String(100), nullable=True)
    date_prepared = db.Column(db.DateTime, nullable=False)
    img_url = db.Column(db.String(100), nullable=False)

    created_by_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    created_by = db.relationship('User')

    recipes = db.relationship(
        'Recipe', secondary="meal_recipes", back_populates='meals')


class Recipe(db.Model):
    __tablename__ = 'recipe'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    description = db.Column(db.String(300), nullable=False)
    ingredients = db.Column(db.String(300), nullable=False)
    process = db.Column(db.String(300), nullable=False)

    created_by_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    created_by = db.relationship('User')

    meals = db.relationship(
        'Meal', secondary='meal_recipes', back_populates="recipes")


meal_recipes_table = db.Table('meal_recipes',
                              db.Column('meal_id', db.Integer,
                                        db.ForeignKey('meal.id')),
                              db.Column('recipe_id', db.Integer,
                                        db.ForeignKey('recipe.id'))
                              )
