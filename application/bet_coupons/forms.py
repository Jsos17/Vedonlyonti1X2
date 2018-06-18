from flask_wtf import FlaskForm
from wtforms import IntegerField, StringField, FieldList, RadioField, validators

def validate_minimum_stake(form, field):
    eur = form.stake_eur.data
    cent = form.stake_cent.data
    if eur == 0 and cent < 10:
        raise validators.ValidationError("Stake must be at least 10 cents")


class Bet_couponForm(FlaskForm):
    stake_eur = IntegerField("Stake eur", validators=[validators.NumberRange(min=0, max=100), validate_minimum_stake])
    stake_cent = IntegerField("Stake cent", validators=[validators.NumberRange(min=0, max=99), validate_minimum_stake])

    class Meta:
        csrf = False
