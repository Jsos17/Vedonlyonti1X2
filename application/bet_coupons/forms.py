from flask_wtf import FlaskForm
from wtforms import DecimalField, HiddenField, validators
from application.money_handler import sum_eur_cent, to_cents

def validate_min_max_stake(form, field):
    try:
        stake = int(100 * form.stake.data)
        if stake > float(form.max_stake.data) * 100:
            raise validators.ValidationError("Your stake is larger than the smallest maximum stake of the selected offers " + form.max_stake.data + " eur")
    except (TypeError, ValueError):
        raise validators.ValidationError("Please, select a stake")

def validate_balance(form, field):
    stake_cents = 0
    balance_cents = 0
    try:
        stake_cents = int(100 * form.stake.data)
        b_eur = int(form.bettor_balance_eur.data)
        b_cent = int(form.bettor_balance_cent.data)
        balance_cents = to_cents(b_eur, b_cent)
    except (TypeError, ValueError):
        raise validators.StopValidation("Please, select a stake")

    if stake_cents > balance_cents:
        raise validators.ValidationError("Your stake exceeds your balance")

def validate_stake_places(form, field):
    if field.data == None:
        raise validators.StopValidation("Field cannot be empty")
    balance_str = str(field.data)
    if balance_str.find(".") != -1:
        split_eur_cent = balance_str.split(".")
        if len(split_eur_cent[1]) > 2:
            raise validators.ValidationError("Only two decimal places allowed")

def validate_acceptable_range_eur(form, field):
    try:
        e = int(field.data)
        if e < 0:
            raise validators.StopValidation("Something went wrong")
    except (TypeError, ValueError):
        raise validators.StopValidation("Something went wrong")

def validate_acceptable_range_cent(form, field):
    try:
        c = int(field.data)
        if c < 0 or c > 99:
            raise validators.StopValidation("Something went wrong")
    except (TypeError, ValueError):
        raise validators.StopValidation("Something went wrong")

def validate_range_max_stake(form, field):
    try:
        s = float(field.data)
        if s < 0.0 or s > 100.0:
            raise validators.StopValidation("Something went wrong")
    except (TypeError, ValueError):
        raise validators.StopValidation("Something went wrong")


class Bet_couponForm(FlaskForm):
    stake = DecimalField("Stake/Eur (minimum = 0.10 Eur)", places = 2, validators=[validators.NumberRange(min=0.10, max=100.0),
                         validate_stake_places, validate_min_max_stake, validate_balance])
    bettor_balance_eur = HiddenField("", validators=[validate_acceptable_range_eur])
    bettor_balance_cent = HiddenField("", validators=[validate_acceptable_range_cent])
    max_stake = HiddenField("", validators=[validate_range_max_stake])

    class Meta:
        csrf = False
