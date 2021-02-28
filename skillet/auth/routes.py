from flask import Blueprint, request, render_template, redirect, url_for, flash
from datetime import date, datetime

from wtforms.validators import Email
from flask_login import login_required, login_user, logout_user
from skillet.models import User
from skillet.auth.forms import SignUpForm, LoginForm
from skillet import bcrypt
from datetime import datetime

# Import app and db from events_app package so that we can run app
from skillet import app, db

auth = Blueprint("auth", __name__, template_folder='templates')

##########################################
#           Auth Routes                  #
##########################################


@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignUpForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(
            form.password.data).decode('utf-8')
        user = User(
            username=form.username.data,
            email=form.email.data,
            password=hashed_password,
            date_created=datetime.now(),
            last_logged_in=datetime.now()
        )

        db.session.add(user)
        db.session.commit()

        # Log the user in after they create their account
        login_user(user, remember=True)

        flash('Account Created.')
        return redirect(url_for('auth.profile', id=user.id))
    print(form.errors)
    return render_template('signup.html', form=form)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):

            login_user(user, remember=True)

            # Update the date of last time user logged in
            user.last_logged_in = datetime.now()
            db.session.add(user)
            db.session.commit()

            next_page = request.args.get('next')

            return redirect(next_page if next_page else url_for('auth.profile', id=user.id))
    print(form.errors)
    return render_template('login.html', form=form)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))


@auth.route('/profile/<id>')
@login_required
def profile(id):
    """Display a user's profile"""
    user = User.query.get(id)

    return render_template('profile.html', user=user)
