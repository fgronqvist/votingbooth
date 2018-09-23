from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, validators
from wtforms.fields.html5 import EmailField

class RegisterForm(FlaskForm):
    firstname = StringField(u"Firstname", [validators.Length(min=2, max=256)])
    lastname = StringField(u"Lastname", [validators.length(min=2, max=256)])
    email = EmailField(u"Email", [validators.InputRequired(), validators.Email()])
    password = PasswordField(u"Password", [validators.InputRequired(), validators.EqualTo('passwordb')])
    passwordb = PasswordField(u"Confirm password")

    class Meta:
        csrf = False

class LoginForm(FlaskForm):
    email = StringField(u"Email", [validators.InputRequired(), validators.Email()])        
    password = PasswordField(u"Password", [validators.InputRequired()])

    class Meta:
        csrf = False