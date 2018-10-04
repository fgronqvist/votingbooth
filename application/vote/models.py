from application import db

class Vote(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date_created = db.Column(db.DateTime(timezone=True), default=db.func.current_timestamp())
    date_modified = db.Column(db.DateTime(timezone=True), default=db.func.current_timestamp(),
    onupdate=db.func.current_timestamp())
    poll_id = db.Column(db.Integer, db.ForeignKey('poll.id'), nullable=False)
    value = db.Column(db.String(256), nullable=False)
