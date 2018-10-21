from application import db
from sqlalchemy.sql import text

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

    @staticmethod
    def admin_top_polls_most_votes(limit=10):
        stmt  = text("""
        SELECT
            t.vote_cnt,
            poll.id,
            poll.name,
            poll.date_open,
            poll.date_close,
            account.id,
            account.firstname,
            account.lastname
        FROM
            (
                SELECT
                    count(*) as vote_cnt,
                    poll_id
                FROM
                    vote
                GROUP BY
                    poll_id
                ORDER BY
                    count(*) desc
                LIMIT :limit
            ) as t
        LEFT JOIN poll ON (t.poll_id = poll.id)
        LEFT JOIN account ON (account.id = poll.owner_id)
        """).params(limit=limit)
        return db.engine.execute(stmt)

    @staticmethod
    def order66():
        res = db.engine.execute("DELETE FROM vote")
        res = db.engine.execute("DELETE FROM user_voted")

class User_voted(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    poll_id = db.Column(db.Integer, db.ForeignKey('poll.id'), nullable=False)
    account_id = db.Column(db.Integer, db.ForeignKey('account.id'), nullable=False)
    date_created = db.Column(db.DateTime(timezone=True), default=db.func.current_timestamp())
