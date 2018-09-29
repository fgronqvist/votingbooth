from application import app, db
from flask import render_template, request, redirect, url_for
from flask_login import login_required, login_user, current_user
from .models import Account
from application.poll.models import Poll
from sqlalchemy import exc

from application.account.forms import RegisterForm, LoginForm

@app.route("/account/", methods=["GET"])
@login_required
def account_index():
    polls = Poll.query.filter_by(owner_id=current_user.id)
    return render_template("account/index.html", polls = polls)

@app.route("/account/login", methods=["POST"])
def account_login():
    login_form = LoginForm(request.form)
    account = Account.query.filter_by(email=login_form.email.data).first()
    if account and account.is_correct_password(login_form.password.data):
        login_user(account)
        return redirect(url_for("account_index"))
    else:
        return render_template("index.html", login_error = True)

@app.route("/account/register", methods=["GET"])
def account_register():
    return render_template("account/register.html", form = RegisterForm())

@app.route("/account/register", methods=["POST"])
def account_registerb():
    form = RegisterForm(request.form)

    if not form.validate():
        return render_template("account/register.html", form = form)

    account = Account(form.firstname.data, form.lastname.data, form.email.data, form.password.data)
    db.session().add(account)
    try:
        db.session().commit()
        return render_template("account/register_done.html")
    except exc.SQLAlchemyError:
        email_error = "email not unique"
        return render_template("account/register.html", form = form, email_error = email_error)