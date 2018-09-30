from flask import render_template
from application import app
from application.account.forms import LoginForm

@app.route("/")
def index():
    form = LoginForm()
    return render_template("index.html", form=form)