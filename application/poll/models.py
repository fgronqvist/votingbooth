from application import db

class Poll(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date_created = db.Column(db.DateTime(timezone=True), default=db.func.current_timestamp())
    date_modified = db.Column(db.DateTime(timezone=True), default=db.func.current_timestamp(),
    onupdate=db.func.current_timestamp())
    name = db.Column(db.String(256), nullable=False)
    owner_id = db.Column(db.Integer, nullable=False)
    date_open = db.Column(db.DateTime(timezone=True))
    date_close = db.Column(db.DateTime(timezone=True))

    def __init__(self, name, owner_id):
        self.name = name
        self.owner_id = owner_id

class Vote(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date_created = db.Column(db.DateTime(timezone=True), default=db.func.current_timestamp())
    date_modified = db.Column(db.DateTime(timezone=True), default=db.func.current_timestamp(),
    onupdate=db.func.current_timestamp())

    poll_id = db.Column(db.Integer, nullable=False)
    value = db.Column(db.String(256), nullable=False)

    def __init__(self, poll_id, value):
        self.poll_id = poll_id
        self.value = value