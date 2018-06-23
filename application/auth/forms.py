from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, IntegerField, DecimalField, HiddenField, validators
from application.auth.models import Bettor
from application.money_handler import to_cents
from passlib.hash import sha256_crypt

def validate_places(form, field):
    if field.data == None:
        raise validators.StopValidation("Field cannot be empty")
    money_str = str(field.data)
    if money_str.find(".") != -1:
        split_eur_cent = money_str.split(".")
        if len(split_eur_cent[1]) > 2:
            raise validators.ValidationError("Only two decimal places allowed")

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
    username = StringField("Username (length 8-144)", [validators.Length(min=8, max=144), validate_username])
    password = PasswordField("Password (length 8-144)", [validators.Length(min=8, max=144), validators.EqualTo('confirm_password', message='Passwords must match')])
    confirm_password = PasswordField("Confirm password")

    class Meta:
        csrf = False

def validate_old_password(form, field):
    b_id = -1
    try:
        b_id = int(form.bettor_id.data)
    except (ValueError, TypeError):
        pass

    if b_id == -1:
        raise validators.ValidationError("Something went wrong")
    else:
        b = Bettor.query.get(b_id)
        if sha256_crypt.verify(form.old_password.data, b.password) == False:
            raise validators.ValidationError("Old password does not match")

class PasswordChangeForm(FlaskForm):
    old_password = PasswordField("Old password", [validate_old_password])
    new_password = PasswordField("New password", [validators.Length(min=8, max=144), validators.EqualTo('new_confirm', message='Passwords must match')])
    new_confirm = PasswordField("Confirm new password")
    bettor_id = HiddenField("")

    class Meta:
        csrf = False

class MoneyInForm(FlaskForm):
    money_in = DecimalField("Deposit: (min = 10.00 eur, max = 10 000.00 eur, format: eur.cent / eur)",
                            places = 2, validators=[validators.NumberRange(min=10.0, max=10000.0), validate_places])

    class Meta:
        csrf = False

def validate_balance(form, field):
    out_cents = 0
    bal_cents = 0
    try:
        out_cents = int(100 * form.money_out.data)
        bal_cents = to_cents(int(form.balance_eur.data), int(form.balance_cent.data))
    except (ValueError, TypeError):
        raise validators.ValidationError("Something went wrong")
        return

    if out_cents > bal_cents:
        raise validators.ValidationError("Your transfer request exceeds your balance")

class MoneyOutForm(FlaskForm):
    money_out = DecimalField("Withdraw: (min = 10.00 eur, max = 10 000.00 eur, format: eur.cent)",
                             places = 2, validators=[validators.NumberRange(min=0.0, max=10000.0), validate_places, validate_balance])
    balance_eur = HiddenField("")
    balance_cent = HiddenField("")

    class Meta:
        csrf = False
