from flask_wtf import FlaskForm
from wtforms import BooleanField, DecimalField, validators

def validate_risk(form, field):
    try:
        ret_percent = 1 / (1/form.odds_1.data + 1/form.odds_x.data + 1/form.odds_2.data)
        if ret_percent > 0.90:
            raise validators.ValidationError("The percentage returned to bettors exceeds 90 %, lower the odds")
    except TypeError:
        raise validators.ValidationError()

class Betting_offerForm(FlaskForm):
    odds_1 = DecimalField("Odds for home win ", places=2, validators=[validators.NumberRange(min=1.00, max=90), validate_risk])
    odds_x = DecimalField("Odds for draw", places=2, validators=[validators.NumberRange(min=1.00, max=90), validate_risk])
    odds_2 = DecimalField("Odds for away win", places=2, validators=[validators.NumberRange(min=1.00, max=90), validate_risk])
    max_stake = DecimalField("Maximum stake (0-100)", [validators.NumberRange(min=0.0,max=100.0)])
    active = BooleanField("The betting offer is active")
    closed = BooleanField("The betting offer is closed")

    class Meta:
        csrf = False
