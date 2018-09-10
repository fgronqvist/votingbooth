from flask import Flask
app = Flask(__name__)

# Init SQLAlchemy
from flask_sqlalchemy import SQLAlchemy
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///votingbooth.db"
app.config["SQLALCHEMY_ECHO"] = True
db = SQLAlchemy(app)

# Setup views
from application import views

# Setup db tables
from application.votes import models
from application.votes import views
db.create_all()