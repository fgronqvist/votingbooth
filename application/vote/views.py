from application import app, db
from flask import render_template, request, redirect, url_for, abort
from flask_login import login_required, current_user
from application.poll.models import Poll, Vote_option
from .models import Vote
from .forms import VoteForm, VoteFormConfirm
from .helpers import hasvoted
from sqlalchemy import exc

@app.route("/vote/<poll_id>", methods=["GET"])
def vote_id(poll_id):
    form = VoteForm(request.form)
    try:
        vote_options = Vote_option.query.filter_by(poll_id=poll_id).order_by(Vote_option.ordernum.asc()).all()
        poll = Poll.query.filter_by(id=poll_id).one()
    except exc.SQLAlchemyError:
        abort(404)

    if hasvoted(poll.id):
        return render_template("vote/hasvoted.html", poll=poll)

    form.poll_id.data = poll.id
    form.vote_options = vote_options

    return render_template("vote/vote.html", poll=poll, form=form)

@app.route("/vote/show_confirm", methods=["POST"])
def show_confirm():
    form = VoteForm(request.form)
    try:   
        vote_option = Vote_option.query.filter_by(id=int(request.form["voteoption"]), poll_id=int(form.poll_id.data)).one()
        poll = Poll.query.filter_by(id=int(form.poll_id.data)).one()
    except exc.SQLAlchemyError:
        abort(404)

    if hasvoted(poll.id):
        return render_template("vote/hasvoted.html", poll=poll)
        
    return render_template("vote/show_confirm.html", poll=poll, vote_option=vote_option, form=form)

@app.route("/vote/confirm", methods=["POST"])
def vote_confirm():
    form = VoteFormConfirm(request.form)
    try:
        poll = Poll.query.filter_by(id=int(form.poll_id.data)).one()
    except exc.SQLAlchemyError as e:
        print(e)
        abort(404)            

    if hasvoted(poll.id):
        return render_template("vote/hasvoted.html", poll=poll)

    if form.validate_on_submit():
        try:
            vote = Vote()
            vote.poll_id = poll.id
            vote.vote_option_id = int(form.selected_option.data)
            db.session.add(vote)
            db.session.commit()
        except exc.SQLAlchemyError as e:
            print(e)
            abort(404)
        
        # Store the poll.id into a cookie to prevent multiple votes (in the same session)
        tpl = render_template("vote/thankyou.html", poll=poll)
        response = app.make_response(tpl)
        cookie = []
        if "vt" in request.cookies:
            cookie = request.cookies.get("vt").split(".")
        cookie.append(poll.id)
        response.set_cookie("vt", ".".join(map(str,cookie)))
        return response
    else:
        return render_template("vote/error.html", poll=poll, form=form)