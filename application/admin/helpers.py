from application import app, db
from flask_login import current_user
from application.poll.models import Poll, Vote_option
from application.vote.models import Vote, User_voted
from application.account.models import Account
import random
from pathlib import Path
from datetime import datetime, timedelta


class adminHelper:
    file_firstname = Path("application/admin") / "firstnames.txt"
    list_firstname = []
    file_surname = Path("application/admin") / "lastnames.txt"
    list_surname = []
    file_words = Path("application/admin") / "words.txt"
    list_words = []
    num_accounts = random.randint(20, 100)
    num_polls = random.randint(100, 300)

    def execute_order66(self):
        # The old shall fall
        Poll.order66()
        Vote.order66()
        Account.order66(neo_is_the_one=current_user.id)

        # and a new power shall rise
        for i in range(self.num_accounts):
            firstname = self.get_firstname()
            surname = self.get_surname()
            email = self.get_email(firstname=firstname, surname=surname)
            password = self.get_pollname()
            #print("name: %s %s (%s)" % (firstname, surname, email))
            a = Account(firstname=firstname, lastname=surname, email=email, password="", skip_password=True)
            db.session.add(a)
            db.session.commit()

        now = datetime.now()
        for i in range(self.num_polls):
            rnd_days = random.randint(10, 90)
            rnd_hours = random.randint(0, 23)
            rnd_min = random.randint(0,59)
            start_d = now - timedelta(days=rnd_days, hours=rnd_hours, minutes=rnd_min)
            start_d = start_d.replace(microsecond=0)

            rnd_days = random.randint(5, 110)
            rnd_hours = random.randint(0, 23)
            rnd_min = random.randint(0,59)
            end_d = start_d + timedelta(days=rnd_days, hours=rnd_hours, minutes=rnd_min)
            end_d = end_d.replace(microsecond=0)
            #print ("start_d: %s" % (start_d.strftime("%d.%m.%Y %H:%M")))
            #print ("end_d: %s" % (end_d.strftime("%d.%m.%Y %H:%M")))

            poll = Poll(Account.get_random_id()[0])
            poll.name = self.get_pollname()
            poll.anynomous = random.randint(0,1)
            poll.date_open = start_d
            poll.date_close = end_d
            db.session.add(poll)
            db.session.commit()
            #print("%d (anon: %d): %s" % (poll.id, poll.anonymous, poll.name))
            order = 1
            for n in range(random.randint(2,15)):
                option = Vote_option()
                option.poll_id = poll.id
                option.name = self.get_pollname(maxwords=3)
                option.ordernum = order
                order = order + 1
                db.session.add(option)
            
            db.session.commit()
                #print("  option: %s" %(option.name))

        #print("num_accounts: %d" % (self.num_accounts))        
        #print("num_polls: %d" % (self.num_polls))

        for v in range(random.randint(500, 1000)):
            poll = Poll.query.filter_by(id=Poll.get_random_id()[0]).first()
            option = Vote_option.query.filter_by(id=Vote_option.get_random_id(poll.id)[0]).first()
            vote = Vote()
            vote.poll_id = poll.id
            vote.vote_option_id = option.id
            db.session.add(vote)
            db.session.commit()
            if poll.anynomous == 0:
                print("Poll anynomous : 0")
                account = Account.query.filter_by(id=Account.get_random_id()[0]).first()
                user_voted = User_voted()
                user_voted.poll_id = poll.id
                user_voted.account_id = account.id
                db.session.add(user_voted)
                db.session.commit()

        # Vote random number of times between 2000 and 10000
        # Pick a random poll
        # Pick a random option from the poll
        # Check if the poll requires account to vote
        #   if yes, pick a random account
        # Vote

    def get_firstname(self):
        if len(self.list_firstname) == 0:
            self.list_firstname = list(open(str(self.file_firstname)))
        return random.choice(self.list_firstname).rstrip()

    def get_surname(self):
        if len(self.list_surname) == 0:
            self.list_surname = list(open(str(self.file_surname)))
        return random.choice(self.list_surname).rstrip()

    def get_email(self, firstname, surname):
        r = firstname.lower()+'.'+surname.lower()
        r = r.replace(u'å', 'a')
        r = r.replace(u'ä', 'a')
        r = r.replace(u'ö', 'o')
        r = r.replace(u'ü', 'u')
        r = r.replace(u'ÿ', 'y')
        r = r.replace(u'é', 'e')
        return r+"@somedomain.net"

    def get_pollname(self, maxwords=5):
        if len(self.list_words) == 0:
            self.list_words = list(open(str(self.file_words)))
        x = random.randint(1,maxwords)
        n = ''
        for i in range(x):
            n = n+' '+random.choice(self.list_words).rstrip()
            if i == 0:
                n = n.title()
                n = n.replace("'S", "'s")
        return n.rstrip()
        
