from flask_wtf import FlaskForm
from wtforms import IntegerField, StringField, validators

class Bet_couponForm(FlaskForm):
    stake_eur = IntegerField("Stake eur", validators=[validators.NumberRange(min=0)])
    stake_cent = IntegerField("Stake cent", validators=[validators.NumberRange(min=0, max=99)])

    class Meta:
        csrf = False
