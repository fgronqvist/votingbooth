from flask_wtf import FlaskForm
from wtforms import StringField, DateTimeField, BooleanField, validators

class PollForm(FlaskForm):
    name = StringField(u"Name", [validators.Length(min=1, max=256)])
    start = DateTimeField(u"start", [validators.Required()])
    end = DateTimeField(u"End", [validators.Required()])    
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
        