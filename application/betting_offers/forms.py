from flask_wtf import FlaskForm
from wtforms import BooleanField, DecimalField, IntegerField, validators

class Betting_offerForm(FlaskForm):
    odds_1 = DecimalField("Odds for home win", places=2, validators=[validators.NumberRange(min=0.00)])
    odds_x = DecimalField("Odds for draw", places=2, validators=[validators.NumberRange(min=0.00)])
    odds_2 = DecimalField("Odds for away win", places=2, validators=[validators.NumberRange(min=0.00)])
    max_stake = IntegerField("Maximum stake", [validators.NumberRange(min=0,max=100)])
    active = BooleanField("The betting offer is active")
    closed = BooleanField("The betting offer is closed")

    class Meta:
        csrf = False
