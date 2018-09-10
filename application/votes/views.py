from application import app, db
from flask import render_template, request, redirect, url_for
from application.votes.models import Vote

@app.route("/votes/", methods=["GET"])
def votes_index():
    return render_template("votes/list.html", votes = Vote.query.all())

@app.route("/vote/new")
def vote_form():
    return render_template("votes/new.html")

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
