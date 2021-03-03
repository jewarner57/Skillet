from enum import unique
from sqlalchemy_utils import URLType
from flask_login import UserMixin
from skillet import db, login_manager


class User(UserMixin, db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(80), nullable=False, unique=True)
    username = db.Column(db.String(80), nullable=False)
    password = db.Column(db.String(200), nullable=False)

    date_created = db.Column(db.DateTime, nullable=False)
    last_active = db.Column(db.DateTime, nullable=False)

    recipes = db.relationship('Recipe', backref='user')
    meals = db.relationship('Meal', backref='user')


class Meal(db.Model):
    __tablename__ = 'meal'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    description = db.Column(db.String(100), nullable=True)
    date_prepared = db.Column(db.DateTime, nullable=False)
    img_url = db.Column(db.String(150), nullable=False)

    created_by_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    recipes = db.relationship(
        'Recipe', secondary="meal_recipes", back_populates='meals')


class Recipe(db.Model):
    __tablename__ = 'recipe'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    description = db.Column(db.String(300), nullable=False)
    ingredients = db.Column(db.String(300), nullable=False)
    instructions = db.Column(db.String(300), nullable=False)

    created_by_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    meals = db.relationship(
        'Meal', secondary='meal_recipes', back_populates="recipes")

    def __repr__(self):
        return self.name.title()


meal_recipes_table = db.Table('meal_recipes',
                              db.Column('meal_id', db.Integer,
                                        db.ForeignKey('meal.id')),
                              db.Column('recipe_id', db.Integer,
                                        db.ForeignKey('recipe.id'))
                              )


@login_manager.user_loader
def load_user(id):
    return User.query.get(id)
