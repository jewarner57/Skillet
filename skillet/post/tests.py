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
# Tests
#################################################


# class MainTests(unittest.TestCase):
#     def setUp(self):
#         """Executed prior to each test."""
#         app.config['TESTING'] = True
#         app.config['WTF_CSRF_ENABLED'] = False
#         app.config['DEBUG'] = False
#         app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
#         self.app = app.test_client()
#         db.drop_all()
#         db.create_all()

#     def test_homepage_logged_out(self):
#         """Test that the books show up on the homepage."""
#         # Set up
#         create_books()
#         create_user()

#         # Make a GET request
#         response = self.app.get('/', follow_redirects=True)
#         self.assertEqual(response.status_code, 200)

#         # Check that page contains all of the things we expect
#         response_text = response.get_data(as_text=True)
#         self.assertIn('To Kill a Mockingbird', response_text)
#         self.assertIn('The Bell Jar', response_text)
#         self.assertIn('me1', response_text)
#         self.assertIn('Log In', response_text)
#         self.assertIn('Sign Up', response_text)

#         # Check that the page doesn't contain things we don't expect
#         # (these should be shown only to logged in users)
#         self.assertNotIn('Create Book', response_text)
#         self.assertNotIn('Create Author', response_text)
#         self.assertNotIn('Create Genre', response_text)

#     def test_homepage_logged_in(self):
#         """Test that the books show up on the homepage."""
#         # Set up
#         create_books()
#         create_user()
#         login(self.app, 'me1', 'password')

#         # Make a GET request
#         response = self.app.get('/', follow_redirects=True)
#         self.assertEqual(response.status_code, 200)

#         # Check that page contains all of the things we expect
#         response_text = response.get_data(as_text=True)
#         self.assertIn('To Kill a Mockingbird', response_text)
#         self.assertIn('The Bell Jar', response_text)
#         self.assertIn('me1', response_text)
#         self.assertIn('Create Book', response_text)
#         self.assertIn('Create Author', response_text)
#         self.assertIn('Create Genre', response_text)

#         # Check that the page doesn't contain things we don't expect
#         # (these should be shown only to logged out users)
#         self.assertNotIn('Log In', response_text)
#         self.assertNotIn('Sign Up', response_text)

#     def test_book_detail_logged_out(self):
#         """Test that the book appears on its detail page."""
#         # Use helper functions to create books, authors, user
#         create_books()
#         create_user()

#         # Make a GET request to the URL /book/1, check to see that the
#         # status code is 200
#         response = self.app.get('/book/1', follow_redirects=True)
#         self.assertEqual(response.status_code, 200)

#         # Check that the response contains the book's title
#         # and author's name
#         response_text = response.get_data(as_text=True)
#         self.assertIn('To Kill a Mockingbird', response_text)
#         self.assertIn('Harper Lee', response_text)
#         self.assertIn('July 11, 1960', response_text)

#         # Check that the response does NOT contain the 'Favorite' button
#         # (it should only be shown to logged in users)
#         self.assertNotIn('Favorite', response_text)

#     def test_book_detail_logged_in(self):
#         """Test that the book appears on its detail page."""
#         # Use helper functions to create books, authors, user, & to log in
#         create_books()
#         create_user()
#         login(self.app, 'me1', 'password')

#         # Make a GET request to the URL /book/1, check to see that the
#         # status code is 200
#         response = self.app.get('/book/1', follow_redirects=True)
#         self.assertEqual(response.status_code, 200)

#         # Check that the response contains the book's title, publish date,
#         # and author's name
#         response_text = response.get_data(as_text=True)
#         self.assertIn('To Kill a Mockingbird', response_text)
#         self.assertIn('Harper Lee', response_text)
#         self.assertIn('July 11, 1960', response_text)

#         # Check that the response contains the 'Favorite' button
#         self.assertIn('Favorite', response_text)

#     def test_update_book(self):
#         """Test updating a book."""
#         # Set up
#         create_books()
#         create_user()
#         login(self.app, 'me1', 'password')

#         # Make POST request with data
#         post_data = {
#             'title': 'Tequila Mockingbird',
#             'publish_date': '1960-07-12',
#             'author': 1,
#             'audience': 'CHILDREN',
#             'genres': []
#         }
#         self.app.post('/book/1', data=post_data)

#         # Make sure the book was updated as we'd expect
#         book = Book.query.get(1)
#         self.assertEqual(book.title, 'Tequila Mockingbird')
#         self.assertEqual(book.publish_date, date(1960, 7, 12))
#         self.assertEqual(book.audience, Audience.CHILDREN)

#     def test_create_book(self):
#         """Test creating a book."""
#         # Set up
#         create_books()
#         create_user()
#         login(self.app, 'me1', 'password')

#         # Make POST request with data
#         post_data = {
#             'title': 'Go Set a Watchman',
#             'publish_date': '2015-07-14',
#             'author': 1,
#             'audience': 'ADULT',
#             'genres': []
#         }
#         self.app.post('/create_book', data=post_data)

#         # Make sure book was updated as we'd expect
#         created_book = Book.query.filter_by(title='Go Set a Watchman').one()
#         self.assertIsNotNone(created_book)
#         self.assertEqual(created_book.author.name, 'Harper Lee')

#     def test_create_book_logged_out(self):
#         """
#         Test that the user is redirected when trying to access the create book
#         route if not logged in.
#         """
#         # Set up
#         create_books()
#         create_user()

#         # Make GET request
#         response = self.app.get('/create_book')

#         # Make sure that the user was redirecte to the login page
#         self.assertEqual(response.status_code, 302)
#         self.assertIn('/login?next=%2Fcreate_book', response.location)

#     def test_create_author(self):
#         """Test creating an author."""
#         # Make a POST request to the /create_author route

#         # Set up
#         create_books()
#         create_user()
#         login(self.app, 'me1', 'password')

#         # Make POST request with data
#         post_data = {
#             'name': "Mark Twain",
#             'biography': 'Mark Twain wrote some book'
#         }
#         self.app.post('/create_author', data=post_data)

#         # Verify that the author was updated in the database
#         created_author = Author.query.filter_by(name='Mark Twain').one()
#         self.assertIsNotNone(created_author)
#         self.assertEqual(created_author.biography,
#                          'Mark Twain wrote some book')

#     def test_create_genre(self):
#         # Make a POST request to the /create_genre route,
#         # Set up
#         create_books()
#         create_user()
#         login(self.app, 'me1', 'password')

#         # Make POST request with data
#         post_data = {'name': "Non Fiction"}
#         self.app.post('/create_genre', data=post_data)

#         # Verify that the genre was updated in the database
#         created_genre = Genre.query.filter_by(name='Non Fiction').one()
#         self.assertIsNotNone(created_genre)

#     def test_profile_page(self):
#         # Make a GET request to the /profile/me1 route
#         create_user()
#         login(self.app, 'me1', 'password')
#         response = self.app.get('/profile/me1')

#         self.assertEqual(response.status_code, 200)
#         response_text = response.get_data(as_text=True)

#         # Verify that the response shows the appropriate user info
#         self.assertIn('You are logged in as me1', response_text)

#     def test_favorite_book(self):
#         # Login as the user me1
#         create_books()
#         create_user()
#         login(self.app, 'me1', 'password')

#         # Make a POST request to the /favorite/1 route
#         self.app.post('/favorite/1')

#         # Verify that the book with id 1 was added to the user's favorites
#         newUser = User.query.filter_by(username='me1').one()
#         book = Book.query.filter_by(id=1).one()
#         self.assertIsNotNone(newUser)
#         self.assertIsNotNone(newUser.favorite_books)
#         self.assertIn(book, newUser.favorite_books)

#     def test_unfavorite_book(self):
#         # Login as the user me1, and add book with id 1 to me1's favorites
#         create_books()
#         create_user()
#         login(self.app, 'me1', 'password')

#         self.app.post('/favorite/1')

#         # Make a POST request to the /unfavorite/1 route
#         self.app.post('/unfavorite/1')

#         # Verify that the book with id 1 was removed from the user's
#         # favorites
#         newUser = User.query.filter_by(username='me1').one()
#         book = Book.query.filter_by(id=1).one()
#         self.assertIsNotNone(newUser)
#         self.assertNotIn(book, newUser.favorite_books)
