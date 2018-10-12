from application import db

class Vote(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date_created = db.Column(db.DateTime(timezone=True), default=db.func.current_timestamp())
    date_modified = db.Column(db.DateTime(timezone=True), default=db.func.current_timestamp(),
    onupdate=db.func.current_timestamp())
    poll_id = db.Column(db.Integer, db.ForeignKey('poll.id'), nullable=False)
    vote_option_id = db.Column(db.Integer, db.ForeignKey('vote_option.id'), nullable=False)

    @staticmethod
    def add_account_vote(account_id, poll_id):
        r = User_voted.query.filter_by(account_id=account_id, poll_id=poll_id).count()
        if(r > 0):
            return False
        
        r = User_voted()
        r.account_id = account_id
        r.poll_id = poll_id
        db.session.add(r)
        db.session.commit()
        return True

class User_voted(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    poll_id = db.Column(db.Integer, db.ForeignKey('poll.id'), nullable=False)
    account_id = db.Column(db.Integer, db.ForeignKey('account.id'), nullable=False)
    date_created = db.Column(db.DateTime(timezone=True), default=db.func.current_timestamp())
