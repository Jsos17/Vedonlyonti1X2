from flask_wtf import FlaskForm
from wtforms import IntegerField, StringField, FieldList, RadioField, HiddenField, validators
from application.money_handler import sum_eur_cent, to_cents

def validate_min_stake(form, field):
    eur = form.stake_eur.data
    cent = form.stake_cent.data
    if eur == 0 and cent < 10:
        raise validators.ValidationError("Stake must be at least 10 cents")

def validate_balance(form, field):
    stake_cents = to_cents(form.stake_eur.data, form.stake_cent.data)
    balance_cents = 0
    try:
        b_eur = int(form.bettor_balance_eur.data)
        b_cent = int(form.bettor_balance_cent.data)
        balance_cents = to_cents(b_eur, b_cent)
    except ValueError:
        raise validators.ValidationError("Something went wrong. If the problem persists, please contact the administrator")
        return

    if stake_cents > balance_cents:
        raise validators.ValidationError("Your stake exceeds your balance")

class Bet_couponForm(FlaskForm):
    stake_eur = IntegerField("Stake eur", validators=[validators.NumberRange(min=0, max=100), validate_min_stake])
    stake_cent = IntegerField("Stake cent", validators=[validators.NumberRange(min=0, max=99), validate_min_stake])
    bettor_balance_eur = HiddenField("", validators=[validate_balance])
    bettor_balance_cent = HiddenField("", validators=[validate_balance])

    class Meta:
        csrf = False
