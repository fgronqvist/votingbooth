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
    anynomous = db.Column(db.Boolean())

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
                    vote.vote_option_id, vote_option.name
                order by
                    count(*) desc """).params(poll_id=poll_id)
        ret = []
        res = db.engine.execute(stmt)
        for row in res:
            ret.append({"vote_count":row[0], "vote_name":row[1]})
        
        return ret

    @staticmethod
    def get_top_polls(owner_id, limit):
        stmt = text("""SELECT
            vote.poll_id, 
            poll.name, 
            count(*) as cnt 
            FROM vote 
            LEFT JOIN poll ON (poll.id = vote.poll_id) 
            GROUP BY vote.poll_id, poll.name 
            ORDER BY count(*) DESC LIMIT :limit
        """).params(limit=limit)
        ret = []
        res = db.engine.execute(stmt)
        for row in res:
            ret.append({"poll_id":row[0], "poll_name":row[1], "vote_count":row[2]})
        return ret

    @staticmethod
    def get_admin_top_polls(limit=10):
        stmt = text("""
        SELECT
            account.id,
            account.firstname,
            account.lastname,
            account.email,
            account.date_created,
            count(*) as poll_cnt
        FROM
            poll
        LEFT JOIN account ON (poll.owner_id = account.id)
        GROUP BY
            account.id
        ORDER BY
            count(*) desc
        LIMIT :limit
        """).params(limit=limit)
        return db.engine.execute(stmt)

    @staticmethod
    def admin_active_vs_inactive_polls(now):
        stmt = text("""
        SELECT
            (SELECT count(*) 
                FROM
                    poll
                WHERE
                    date_open <= :now
                AND
                    date_close >= :now
            ) AS open,
            (SELECT count(*) 
                FROM
                    poll
                WHERE
                    date_open >= :now
                OR
                    date_close < :now
                ) AS closed,
            count(*) AS total
            FROM
            poll
        """).params(now=now.now())
        return db.engine.execute(stmt)

    @staticmethod
    def get_random_id():
        stmt = text("SELECT id FROM poll ORDER BY RANDOM() LIMIT 1")
        res = db.engine.execute(stmt)
        return res.first()


    @staticmethod
    def order66():
        res = db.engine.execute("DELETE FROM poll")
        res = db.engine.execute("DELETE FROM vote_option")
        

class Vote_option(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    poll_id = db.Column(db.Integer, db.ForeignKey('poll.id'), nullable=False)
    ordernum = db.Column(db.Integer, nullable=False)
    name = db.Column(db.String(256), nullable=False)

    @staticmethod
    def get_random_id(poll_id):
        stmt = text("""SELECT 
            id 
        FROM 
            vote_option
        WHERE 
            poll_id = :poll_id 
        ORDER BY RANDOM() LIMIT 1""").params(poll_id=poll_id)
        res = db.engine.execute(stmt)
        return res.first()
