from flask_wtf import FlaskForm
from wtforms import StringField, DateField, BooleanField, IntegerField, HiddenField, SelectField, validators, ValidationError
from datetime import datetime


class PollForm(FlaskForm):
    def time_range(max=24):
        r = []
        for i in range(max):
            t = ('{}'.format(i), '{:02d}'.format(i))
            r.append(t)
        return r

    poll_id = HiddenField(u"poll_id")
    name = StringField(u"Name", [validators.Length(min=1, max=256)])
    start_date = DateField(u"Start date", [validators.InputRequired()], format="%d.%m.%Y")
    start_hour = SelectField(u"Start hour", choices=time_range(24))
    start_minute = SelectField(u"Start minute", choices=time_range(60))
    end_date = DateField(u"End", [validators.Required()], format="%d.%m.%Y")    
    end_hour = SelectField(u"End hour", choices=time_range(24))
    end_minute = SelectField(u"End minute", choices=time_range(60))
    delete = BooleanField(u"Delete")

    class Meta:
        csrf = False

    def validate(self):
        try:
            d = datetime.strftime(self.start_date.data, "%d.%m.%Y")
            d = d +" "+str(self.start_hour.data)+":"+str(self.start_minute.data)
            start = datetime.strptime(d, "%d.%m.%Y %H:%M")
            d = datetime.strftime(self.end_date.data, "%d.%m.%Y")
            d = d +" "+str(self.end_hour.data)+":"+str(self.end_minute.data)
            end = datetime.strptime(d, "%d.%m.%Y %H:%M")

            if not FlaskForm.validate(self):
                return False
            if start >= end:
                errors = list(self.start_date.errors) 
                errors.append("Start time is larger or equals end time?!?")
                self.start_date.errors = errors
                errors = list(self.end_date.errors) 
                errors.append("Start time is larger or equals end time?!?")
                self.end_date.errors = errors
                return False
            else:
                return True
        except:
            errors = list(self.start_date.errors) 
            errors.append("There was something strange about your start and end times!?! Please check them.")
            self.start_date.errors = errors
            errors = list(self.end_date.errors) 
            errors.append("There was something strange about your start and end times!?! Please check them.")
            self.end_date.errors = errors
            return False
        
class VoteOptionForm(FlaskForm):
    name = StringField(u"Name", [validators.Length(min=1, max=256)])

    class Meta:
        csrf = False
