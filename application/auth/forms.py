from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, IntegerField, validators
from application.auth.models import Bettor

class LoginForm(FlaskForm):
    username = StringField("Username")
    password = PasswordField("Password")

    class Meta:
        csrf = False

def validate_username(form, field):
    bettor = Bettor.query.filter_by(username=form.username.data).first()
    if bettor != None:
        raise validators.ValidationError("Username exists already")

class BettorForm(FlaskForm):
    username = StringField("Username", [validators.Length(min=8, max=144), validate_username])
    password = PasswordField("Password", [validators.Length(min=8, max=144)])
    balance_eur = IntegerField("Initial balance/Eur", [validators.NumberRange(min=0, max=9999)])
    balance_cent = IntegerField("Initial balance/Cent", [validators.NumberRange(min=0, max=99)])

    class Meta:
        csrf = False