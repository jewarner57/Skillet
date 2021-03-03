from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from skillet.config import Config
from flask_bcrypt import Bcrypt
import os

app = Flask(__name__)
app.config.from_object(Config)
app.secret_key = os.urandom(24)

db = SQLAlchemy(app)

# Auth setup
login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.init_app(app)

bcrypt = Bcrypt(app)

# blueprints
from skillet.main.routes import main
from skillet.auth.routes import auth
from skillet.post.routes import post

app.register_blueprint(main)
app.register_blueprint(auth)
app.register_blueprint(post)

with app.app_context():
    db.create_all()
