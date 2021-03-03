import os
from unittest import TestCase

from datetime import datetime

from skillet import app, db, bcrypt
from skillet.models import Meal, Recipe, User
"""
Run these tests with the command:
python -m unittest skillet.post.tests
"""

#################################################
# Setup
#################################################


def create_meals():
    r1 = Recipe(name='Test Recipe 1', description="Description",
                ingredients="Ingredients", instructions="Instructions")
    m1 = Meal(name='Test Meal 1', date_prepared=datetime.now(),
              img_url='https://image.com/url')

    m1.recipes.append(r1)
    db.session.add(m1)

    r2 = Recipe(name='Test Recipe 2', description="Description",
                ingredients="Ingredients", instructions="Instructions")
    m2 = Meal(name='Test Meal 2', date_prepared=datetime.now(),
              img_url='https://image.com/url')

    m1.recipes.append(r2)

    db.session.add(m2)
    db.session.commit()


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
# Post Tests
#################################################


class MainTests(TestCase):
    def setUp(self):
        """Executed prior to each test."""
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['DEBUG'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.app = app.test_client()
        db.drop_all()
        db.create_all()

    def test_create_meal(self):
        """Test creating a meal."""
        # Set up
        create_meals()
        create_user()
        login(self.app, 'testing_user@mail.io', 'password')

        # Make POST request with data
        post_data = {
            'name': 'This is a test meal',
            'description': 'This is a test description',
            'date_prepared': datetime.now(),
            'img_url': 'https://www.img_url.com/image'
        }
        self.app.post('/create_meal', data=post_data)

        # Make sure the meal was created correctly
        created_meal = Meal.query.filter_by(name='This is a test meal').one()
        self.assertIsNotNone(created_meal)
        self.assertEqual(created_meal.description,
                         'This is a test description')

    def test_create_meal_logged_out(self):
        """
        Test that the user is redirected when trying to access the create meal
        route if not logged in.
        """
        # Make POST request with data for create meal
        post_data = {
            'name': 'This is a test meal',
            'description': 'This is a test description',
            'date_prepared': datetime.now(),
            'img_url': 'https://www.img_url.com/image'
        }
        response = self.app.post('/create_meal', data=post_data)

        # Make sure that the user was redirected to the login page
        self.assertEqual(response.status_code, 302)
        self.assertIn('/login?next=%2Fcreate_meal', response.location)

    def test_create_recipe(self):
        """Test creating a recipe."""
        # Set up
        create_meals()
        create_user()
        login(self.app, 'testing_user@mail.io', 'password')

        # Make POST request with data
        post_data = {
            'name': 'This is a test meal',
            'description': 'This is a test description',
            'ingredients': 'Put this in the food',
            'instructions': 'Here are instructions',
        }
        self.app.post('/create_recipe', data=post_data)

        # Make sure the meal was created correctly
        created_recipe = Recipe.query.filter_by(
            name='This is a test meal').one()
        self.assertIsNotNone(created_recipe)
        self.assertEqual(created_recipe.description,
                         'This is a test description')
        self.assertEqual(created_recipe.ingredients,
                         'Put this in the food')

    def test_profile_page(self):
        # Make a GET request to the /profile/me1 route
        create_user()
        login(self.app, 'testing_user@mail.io', 'password')
        response = self.app.get('/profile/1')

        self.assertEqual(response.status_code, 200)
        response_text = response.get_data(as_text=True)

        # Verify that the response shows the appropriate user info
        self.assertIn("Test_User's Profile", response_text)
        self.assertIn("testing_user@mail.io", response_text)

    def test_edit_meal(self):
        """Test updating a meal."""
        # Set up
        create_user()
        login(self.app, 'testing_user@mail.io', 'password')

        # create a new meal
        post_data = {
            'name': 'This is a test meal',
            'description': 'This is a test description',
            'date_prepared': datetime.now(),
            'img_url': 'https://www.img_url.com/image'
        }
        self.app.post('/create_meal', data=post_data)

        # Make POST request with data
        post_data = {
            'name': 'Meal Name',
            'description': 'This is a test description that was edited',
            'img_url': 'https://www.img_url.com/image'
        }
        self.app.post('/edit_meal/1', data=post_data)

        # Make sure the book was updated as we'd expect
        meal = Meal.query.get(1)
        self.assertNotEqual(meal, None)
        self.assertEqual(meal.description,
                         'This is a test description that was edited')
        self.assertEqual(meal.name, 'Meal Name')
