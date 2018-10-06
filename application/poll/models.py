from application import db
from sqlalchemy.sql import text

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

    @staticmethod
    def get_vote_breakdown(owner_id, poll_id):
        stmt = text("""select
                    count(*) as vote_count,
                    vote_option.name as vote_name
                from
                    vote
                left join vote_option on (vote.vote_option_id = vote_option.id)
                where vote.poll_id = :poll_id
                group by 
                    vote.vote_option_id
                order by
                    count(*) desc """).params(poll_id=poll_id)
        ret = []
        res = db.engine.execute(stmt)
        for row in res:
            ret.append({"vote_count":row[0], "vote_name":row[1]})
        
        return ret


class Vote_option(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    poll_id = db.Column(db.Integer, db.ForeignKey('poll.id'), nullable=False)
    ordernum = db.Column(db.Integer, nullable=False)
    name = db.Column(db.String(256), nullable=False)