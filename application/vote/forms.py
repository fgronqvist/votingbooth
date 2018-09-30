from flask_wtf import FlaskForm
from wtforms import StringField, DateField, BooleanField, IntegerField, RadioField, HiddenField, validators

class VoteForm(FlaskForm):
    poll_id = HiddenField(u"poll_id", [validators.Required()])
    vote_options = RadioField(u"option")

class VoteFormConfirm(FlaskForm):
    poll_id = HiddenField(u"poll_id", [validators.Required()])
    selected_option = IntegerField(u"selected_option", [validators.Required()])