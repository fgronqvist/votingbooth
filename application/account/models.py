from application import db, bcrypt
from sqlalchemy.sql import text

class Account(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date_created = db.Column(db.DateTime(timezone=True), default=db.func.current_timestamp())
    date_modified = db.Column(db.DateTime(timezone=True), default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())
    firstname = db.Column(db.String(256), nullable=False)
    lastname = db.Column(db.String(256), nullable=False)
    email = db.Column(db.String(256), nullable=False, unique=True)
    password = db.Column(db.String(256), nullable=False)
    polls = db.relationship("Poll", backref="owner", lazy=True)
    roles = db.relationship("Account_role", backref="account", lazy=True)

    @staticmethod
    def order66(neo_is_the_one):
        stmt = text("DELETE FROM account WHERE id !=:neo").params(neo=int(neo_is_the_one))
        res = db.engine.execute(stmt)

    @staticmethod
    def get_random_id():
        stmt = text("SELECT id FROM account ORDER BY RANDOM() LIMIT 1")
        res = db.engine.execute(stmt)
        return res.first()

    def __init__(self, firstname, lastname, email, password, skip_password=False):
        self.firstname = firstname
        self.lastname = lastname
        self.email = email
        if skip_password == False:
            self._set_password(password)
        else:
            self.password = "X"

    def _set_password(self, plaintext):
        self.password = bcrypt.generate_password_hash(plaintext).decode('utf-8')

    def is_correct_password(self, plaintext):
        return bcrypt.check_password_hash(self.password, plaintext)

    def is_active(self):
        return True

    def is_anonymous(self):
        return False
    
    def is_authenticated(self):
        return True

    def get_id(self):
        return self.id

    def has_role(self, role):
        role = role.upper()
        for r in self.roles:
            print("r: %s" % (r.name))
            if role == r.name:
                return True
        return False


class Account_role(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    account_id = db.Column(db.Integer, db.ForeignKey("account.id"), nullable=False)
    name = db.Column(db.String(256), nullable=False)

    def __init__(self, role):
        self.name = role.upper()
   
