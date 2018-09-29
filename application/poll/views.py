from application import app, db
from flask import render_template, request, redirect, url_for, abort
from flask_login import login_required, current_user
from .models import Vote, Poll, Vote_option
from .forms import PollForm, VoteOptionForm
from sqlalchemy import exc
from datetime import datetime

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
        return redirect(url_for("account_index"))
    else:
        return render_template("poll/poll.html", form = form, action_url = url_for("poll_new"), poll = poll)

@app.route("/poll/edit/<poll_id>", methods=["POST", "GET"])
@login_required
def poll_edit(poll_id):
    form = PollForm(request.form)
    vote_option_form = VoteOptionForm()
    try:
        poll = Poll.query.filter_by(id=poll_id, owner_id=current_user.id).one()
        vote_options = Vote_option.query.filter_by(poll_id=poll_id).order_by(Vote_option.ordernum)
        if form.delete.data:
            db.session.delete(poll)
            db.session.commit()
            return redirect(url_for("account_index"))
    except exc.SQLAlchemyError:
        abort(404)

    if form.validate_on_submit():
        # Update existing poll
        poll.name = form.name.data
        d = datetime.strftime(form.start_date.data, "%d.%m.%Y")
        d = d +" "+str(form.start_hour.data)+":"+str(form.start_minute.data)
        print(d)
        poll.date_open = datetime.strptime(d, "%d.%m.%Y %H:%M")
        d = datetime.strftime(form.end_date.data, "%d.%m.%Y")
        d = d +" "+str(form.end_hour.data)+":"+str(form.end_minute.data)
        print(d)
        poll.date_close = datetime.strptime(d, "%d.%m.%Y %H:%M")
        db.session.add(poll)
        db.session.commit()
        return redirect(url_for("account_index"))
    else:
        # Show data (first load or if the form validation fails)
        # form = PollForm(request.form)
        form.name.data = poll.name
        form.start_date.data = poll.date_open
        form.start_hour.data = datetime.strftime(poll.date_open, "%-H")
        form.start_minute.data = datetime.strftime(poll.date_open, "%-M")
        form.end_date.data = poll.date_close
        form.end_hour.data = datetime.strftime(poll.date_close, "%-H")
        form.end_minute.data = datetime.strftime(poll.date_close, "%-M")
        return render_template("poll/poll.html", form = form, action_url = url_for("poll_edit", poll_id = poll_id),
            poll = poll, vote_option_form=vote_option_form, vote_options=vote_options)

@app.route("/poll/new_alternative/<poll_id>", methods=["POST"])
@login_required
def new_alternative(poll_id):
    form = VoteOptionForm(request.form)
    try:
        poll = Poll.query.filter_by(id=poll_id, owner_id=current_user.id).one()
    except exc.SQLAlchemyError:
        abort(404)
    if form.validate_on_submit():
        try:
            previous_vote_option = Vote_option.query.filter_by(poll_id=poll.id).order_by(Vote_option.ordernum.desc()).first()
            if(previous_vote_option):
                max_ordernum = previous_vote_option.ordernum +1
            else:
                # NoResultFound
                max_ordernum = 0
        except exc.SQLAlchemyError:
            abort(404)
        
        vote_option = Vote_option()
        vote_option.name = form.name.data
        vote_option.poll_id = poll.id
        vote_option.ordernum = max_ordernum
        db.session.add(vote_option)
        db.session.commit()
        return redirect(url_for("poll_edit", poll_id=poll.id))
    
@app.route("/poll/save_alternative_order/<poll_id>", methods=["POST"])
@login_required
def save_alternative_order(poll_id):
    try:
        poll = Poll.query.filter_by(id=poll_id, owner_id=current_user.id).one()
        vote_options = Vote_option.query.filter_by(poll_id=poll_id).all()
    except exc.SQLAlchemyError:
        abort(404)
    
    place = 0
    order_tbl = {}
    for order in request.form.getlist("opt[]"):
        order_tbl[int(order)] = place
        place = place + 1
    
    for opt in vote_options:
        opt.ordernum = order_tbl[opt.id]
        print(opt)
        db.session.add(opt)
        db.session.commit()

    #print(order_tbl)
    # {1: 0, 2: 1}
    #opt[]=2&opt[]=1&opt[]=3&opt[]=4
    #return redirect(url_for("poll_edit", poll_id=poll.id))
    return ""

@app.route("/poll/delete_alternative/", methods=["GET"])
@login_required
def delete_alternative():
    poll = Poll.query.filter_by(id=int(request.args['poll_id']), owner_id=current_user.id).one()
    vote_option = Vote_option.query.filter_by(id=int(request.args['option_id']), poll_id=poll.id).one()
    db.session.delete(vote_option)
    db.session.commit()
    return redirect(url_for("poll_edit", poll_id=poll.id))

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
