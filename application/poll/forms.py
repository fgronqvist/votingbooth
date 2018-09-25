from flask_wtf import FlaskForm
from wtforms import StringField, DateTimeField, BooleanField, IntegerField, validators

class PollForm(FlaskForm):
    name = StringField(u"Name", [validators.Length(min=1, max=256)])
    start_date = DateTimeField(u"Start date", [validators.Required()])
    start_hour = IntegerField(u"Start hour", [validators.Required(), validators.NumberRange(min=1, max=23)])
    start_minute = IntegerField(u"Start minute", [validators.Required(), validators.NumberRange(min=0, max=59)])
    end_date = DateTimeField(u"End", [validators.Required()])    
    end_hour = IntegerField(u"End hour", [validators.Required(), validators.NumberRange(min=1, max=23)])
    end_minute = IntegerField(u"End minute", [validators.Required(), validators.NumberRange(min=0, max=59)])
    delete = BooleanField(u"Delete")

    class Meta:
        csrf = False

    def validate(self):
        if not FlaskForm.validate(self):
            return False
        if self.start.data >= self.end.data:
            return False
        else:
            return True
        