from application import app, db
from flask import render_template, request, redirect, url_for, abort
from flask_login import login_required, current_user
from application.poll.models import Poll, Vote_option
from .models import Vote
from .forms import VoteForm, VoteFormConfirm
from sqlalchemy import exc

@app.route("/vote/<poll_id>", methods=["GET"])
def vote_id(poll_id):
    form = VoteForm(request.form)
    try:
        vote_options = Vote_option.query.filter_by(poll_id=poll_id).order_by(Vote_option.ordernum.asc()).all()
        poll = Poll.query.filter_by(id=poll_id).one()
    except exc.SQLAlchemyError:
        abort(404)

    form.poll_id.data = poll.id
    form.vote_options = vote_options

    return render_template("vote/vote.html", poll=poll, form=form)

@app.route("/vote/show_confirm", methods=["POST"])
def show_confirm():
    form = VoteForm(request.form)
    #print("XXXXXXXXXXXXXXXXX")
    #print(request.form.getlist("voteoption"))
    #print("XXXXXXXXXXXXXXXXX")
    try:   
        vote_option = Vote_option.query.filter_by(id=int(request.form["voteoption"]), poll_id=int(form.poll_id.data)).one()
        poll = Poll.query.filter_by(id=int(form.poll_id.data)).one()
    except exc.SQLAlchemyError:
        abort(404)

    return render_template("vote/show_confirm.html", poll=poll, vote_option=vote_option, form=form)

@app.route("/vote/confirm", methods=["POST"])
def vote_confirm():
    form = VoteFormConfirm(request.form)
    try:
        poll = Poll.query.filter_by(id=int(form.poll_id.data)).one()
    except exc.SQLAlchemyError:
        abort(404)            

    if form.validate_on_submit():
        try:
            vote = Vote()
            vote.poll_id = poll.id
            vote.value = form.selected_option.data
            db.session.add(vote)
            db.session.commit()
        except exc.SQLAlchemyError:
            abort(404)    
        return render_template("vote/thankyou.html", poll=poll)
    else:
        return render_template("vote/error.html", poll=poll, form=form)