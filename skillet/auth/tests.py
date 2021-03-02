import os
from unittest import TestCase

from datetime import datetime

from skillet import app, db, bcrypt
from skillet.models import Meal, Recipe, User
"""
Run these tests with the command:
python -m unittest skillet.auth.tests
"""

#################################################
# Setup
#################################################


def create_user():
    password_hash = bcrypt.generate_password_hash('password').decode('utf-8')
    user = User(email="testing_user@mail.io",
                username='test_user', password=password_hash,
                date_created=datetime.now(), last_active=datetime.now())

    db.session.add(user)
    db.session.commit()


def login(client, email, password):
    return client.post('/login',
                       data=dict(email=email, password=password),
                       follow_redirects=True)


def logout(client):
    return client.get('/logout', follow_redirects=True)


#################################################
# Auth Tests
#################################################


class AuthTests(TestCase):
    def setUp(self):
        """Executed prior to each test."""
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['DEBUG'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.app = app.test_client()
        db.drop_all()
        db.create_all()

    """Tests for authentication (login & signup)."""

    def test_signup(self):
        # Make a POST to signup
        post_data = {'email': 'test_user_1@mail.io',
                     'username': 'test_user', 'password': 'test'}
        self.app.post('/signup', data=post_data)

        # Check if new user exists
        newUser = User.query.filter_by(email='test_user_1@mail.io').one()
        self.assertIsNotNone(newUser)

    def test_signup_existing_user(self):
        # Make POST request to singup
        post_data = {'email': 'test_user_2@mail.io',
                     'username': 'test_user', 'password': 'test'}
        self.app.post('/signup', data=post_data)

        # Make a POST request to signup the same user again
        post_data = {'email': 'test_user_2@mail.io',
                     'username': 'test_user', 'password': 'test'}
        response = self.app.post('/signup', data=post_data)

        # Get the response page
        response_text = response.get_data(as_text=True)

        self.assertEqual(response.status_code, 200)
        self.assertIn("That email is already associated with another account.",
                      response_text)

    def test_login_right_password(self):
        # Create new user
        create_user()

        # Login with correct credentials
        response = login(self.app, 'testing_user@mail.io', 'password')

        response_text = response.get_data(as_text=True)

        self.assertNotIn("login", response_text)
        self.assertIn("logout", response_text)

    def test_login_nonexistent_user(self):
        # Try to login with non existent user
        response = login(self.app, 'test_user@mail.io', 'password')

        response_text = response.get_data(as_text=True)

        # Check request was successful
        self.assertEqual(response.status_code, 200)

        # Check that login attempt failed
        self.assertIn("No user found with that email.",
                      response_text)
        self.assertIn('Log In', response_text)
        self.assertIn('Login', response_text)

    def test_login_wrong_password(self):
        # Create a new user
        create_user()
        # Login with the wrong password
        response = login(self.app, 'testing_user@mail.io', 'not the password')

        response_text = response.get_data(as_text=True)

        self.assertIn("Invalid Username or Password",
                      response_text)

        self.assertIn('Login', response_text)
        self.assertIn('Log In', response_text)

    def test_logout(self):

        create_user()

        response = login(self.app, 'test_user@mail.io', 'password')

        response = logout(self.app)

        response_text = response.get_data(as_text=True)

        self.assertNotIn("Logout", response_text)
