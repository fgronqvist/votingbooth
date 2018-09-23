from application import app, db
from flask import render_template, request, redirect, url_for
from flask_login import login_required, login_user, current_user
from .models import User
from application.poll.models import Poll
from sqlalchemy import exc

from application.user.forms import RegisterForm, LoginForm

@app.route("/user/", methods=["GET"])
@login_required
def user_index():
    polls = Poll.query.filter_by(owner_id=current_user.id)
    return render_template("user/index.html", polls = polls)

@app.route("/user/login", methods=["POST"])
def user_login():
    login_form = LoginForm(request.form)
    user = User.query.filter_by(email=login_form.email.data).first()
    if user and user.is_correct_password(login_form.password.data):
        login_user(user)
        return redirect(url_for("user_index"))
    else:
        return render_template("index.html", login_error = True)

@app.route("/user/register", methods=["GET"])
def user_register():
    return render_template("user/register.html", form = RegisterForm())

@app.route("/user/register", methods=["POST"])
def user_registerb():
    form = RegisterForm(request.form)

    if not form.validate():
        return render_template("user/register.html", form = form)

    user = User(form.firstname.data, form.lastname.data, form.email.data, form.password.data)
    db.session().add(user)
    try:
        db.session().commit()
        return render_template("user/register_done.html")
    except exc.SQLAlchemyError:
        email_error = "email not unique"
        return render_template("user/register.html", form = form, email_error = email_error)