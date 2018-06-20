from flask_wtf import FlaskForm
from wtforms import IntegerField, StringField, FieldList, RadioField, HiddenField, validators
from application.money_handler import sum_eur_cent, to_cents

def validate_min_max_stake(form, field):
    eur = form.stake_eur.data
    cent = form.stake_cent.data
    if eur == 0 and cent < 10:
        raise validators.ValidationError("Stake must be at least 10 cents")
        return

    stake = to_cents(eur, cent)
    if stake > float(form.max_stake.data) * 100:
        raise validators.ValidationError("Your stake is larger than the smallest maximum stake of the selected offers " + form.max_stake.data + " eur")

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

def validate_acceptable_range(form, field):
    return

class Bet_couponForm(FlaskForm):
    stake_eur = IntegerField("Stake eur", validators=[validators.NumberRange(min=0, max=100), validate_min_max_stake, validate_balance])
    stake_cent = IntegerField("Stake cent", validators=[validators.NumberRange(min=0, max=99), validate_min_max_stake, validate_balance])
    bettor_balance_eur = HiddenField("", validators=[validate_acceptable_range])
    bettor_balance_cent = HiddenField("", validators=[validate_acceptable_range])
    max_stake = HiddenField("", validators=[validate_acceptable_range])

    class Meta:
        csrf = False
