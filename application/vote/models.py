from application import db

class Vote(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date_created = db.Column(db.DateTime(timezone=True), default=db.func.current_timestamp())
    date_modified = db.Column(db.DateTime(timezone=True), default=db.func.current_timestamp(),
    onupdate=db.func.current_timestamp())
    poll_id = db.Column(db.Integer, db.ForeignKey('poll.id'), nullable=False)
    vote_option_id = db.Column(db.Integer, db.ForeignKey('vote_option.id'), nullable=False)
