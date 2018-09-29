from flask import Flask
app = Flask(__name__)

# Init debug toolbar
from flask_debugtoolbar import DebugToolbarExtension
app.config['SECRET_KEY'] = "develdeveldeveldevel"
toolbar = DebugToolbarExtension(app)

# Init SQLAlchemy
from flask_sqlalchemy import SQLAlchemy
import os
if os.environ.get("HEROKU"):
    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL")
else:
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///votingbooth.db"
    app.config["SQLALCHEMY_ECHO"] = True

db = SQLAlchemy(app)

# Init bcrypt
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)
BCRYPT_LOG_ROUNDS = 12

# Init app modules
from application import views
from application.account import views
from application.account import models
from application.account.models import Account
from application.poll import views
from application.poll import models

try:
    db.create_all()
except:
    pass

# Init login manager
from flask_login import LoginManager
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "index"

@login_manager.user_loader
def load_user(userid):
    return Account.query.filter(Account.id==userid).first()