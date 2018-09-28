from application import app, db
from flask import render_template, request, redirect, url_for, abort
from flask_login import login_required, current_user
from .models import Vote, Poll
from .forms import PollForm
from sqlalchemy import exc

@app.route("/poll/new", methods=["GET", "POST"])
@login_required
def poll_new():
    form = PollForm(request.form)
    poll = Poll(form.name.data, current_user.id)
    if form.validate_on_submit():
        poll.date_open = form.start.data
        poll.date_close = form.end.data
        db.session.add(poll)
        db.session.commit()
        return redirect(url_for("user_index"))
    else:
        return render_template("poll/poll.html", form = form, action_url = url_for("poll_new"), poll = poll)

@app.route("/poll/edit/<poll_id>", methods=["POST", "GET"])
@login_required
def poll_edit(poll_id):
    form = PollForm(request.form)
    try:
        poll = Poll.query.filter_by(id=poll_id, owner_id=current_user.id).one()
        if form.delete.data:
            db.session.delete(poll)
            db.session.commit()
            return redirect(url_for("user_index"))
    except exc.SQLAlchemyError:
        abort(404)

    if form.validate_on_submit():
        # Update existing poll
        poll.name = form.name.data
        poll.date_open = form.start.data
        poll.date_close = form.end.data
        db.session.add(poll)
        db.session.commit()
        return redirect(url_for("user_index"))
    else:
        # Show data (first load or if the form validation fails)
        form = PollForm(request.form)
        form.name.data = poll.name
        form.start_date.data = poll.date_open
        form.end_date.data = poll.date_close
        return render_template("poll/poll.html", form = form, action_url = url_for("poll_edit", poll_id = poll_id),
            poll = poll)


@app.route("/votes/", methods=["GET"])
def votes_index():
    return render_template("poll/vote_list.html", votes = Vote.query.all())

@app.route("/vote/new")
def vote_form():
    return render_template("poll/vote_new.html")

@app.route("/votes/", methods=["POST"])
def vote_create():
    vote = Vote(request.form.get("poll_id"), request.form.get("vote_value"))
    db.session.add(vote)
    db.session.commit()
    return redirect(url_for("votes_index"))

@app.route("/vote/<vote_id>/", methods=["POST"])
def nullify_vote(vote_id):
    v = Vote.query.get(vote_id)
    v.value = "NULLIFIED"
    db.session.commit()
    return redirect(url_for("votes_index"))
