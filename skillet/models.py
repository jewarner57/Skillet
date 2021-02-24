from enum import unique
from sqlalchemy_utils import URLType
from flask_login import UserMixin
from skillet import db


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(80), nullable=False, unique=True)
    username = db.Column(db.String(80), nullable=False)
    password = db.Column(db.String(200), nullable=False)

    # TODO - add: last date logged in, and date account created

    def __str__(self):
        return self.username

    def __repr__(self):
        return self.username
