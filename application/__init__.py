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

# Init login manager
from flask_login import LoginManager, current_user
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "index"

from functools import wraps
def login_required(role="ANY"):
    def wrapper(fn):
        @wraps(fn)
        def decorated_view(*args, **kwargs):
            if not current_user:
                return login_manager.unauthorized()
           
            if not current_user.is_authenticated:
                return login_manager.unauthorized()

            unauthorized = False

            if role != "ANY":
                unauthorized = True
                
                for user_role in current_user.roles:
                    if user_role.name == role:
                        unauthorized = False
                        break

            if unauthorized:
                return login_manager.unauthorized()
            
            return fn(*args, **kwargs)
        return decorated_view
    return wrapper

@login_manager.user_loader
def load_user(userid):
    return Account.query.filter(Account.id==userid).first()

# Init app modules
from application import views
from application.account import views
from application.account import models
from application.account.models import Account
from application.poll import views, models
from application.vote import views, models
from application.admin import views

db.create_all()

# Date format snippet
from datetime import datetime
def format_datetime(val, format='medium'):
    if not val:
        return
    if format == 'full':
        format="EEEE, d. MMMM y 'at' HH:mm"
    elif format == 'medium':
        format="%d.%m.%Y %H:%M"

    if isinstance(val, type(datetime.date)):
        return val.strftime(format)
    else: 
        # Remove annoying microseconds if they are present
        val = val.split(".", 1)[0]
        d = datetime.strptime(val, '%Y-%m-%d %H:%M:%S')
        return d.strftime(format)

app.jinja_env.filters['datetime'] = format_datetime