from flask import render_template, redirect, url_for
from flask_login import current_user
from application import app
from application.account.forms import LoginForm

@app.route("/")
def index():
    if current_user.is_authenticated:
        return redirect(url_for("account_index"))
    form = LoginForm()
    return render_template("index.html", form=form)

@app.route("/about")
def about():
    return render_template("about.html")

# a simple layout to test css problems etc
@app.route("/layoutest")
def layoutest():
    return render_template("layoutest.html")