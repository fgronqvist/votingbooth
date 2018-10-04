from application import db

class Poll(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date_created = db.Column(db.DateTime(timezone=True), default=db.func.current_timestamp())
    date_modified = db.Column(db.DateTime(timezone=True), default=db.func.current_timestamp(),
    onupdate=db.func.current_timestamp())
    name = db.Column(db.String(256), nullable=False)
    owner_id = db.Column(db.Integer, db.ForeignKey("account.id"), nullable=False)
    date_open = db.Column(db.DateTime(timezone=True))
    date_close = db.Column(db.DateTime(timezone=True))

    options = db.relationship("Vote_option", backref="poll", lazy=True)
    votes = db.relationship("Vote", backref="poll", lazy=True)

    def __init__(self, owner_id):
        self.owner_id = owner_id

class Vote_option(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    poll_id = db.Column(db.Integer, db.ForeignKey('poll.id'), nullable=False)
    ordernum = db.Column(db.Integer, nullable=False)
    name = db.Column(db.String(256), nullable=False)