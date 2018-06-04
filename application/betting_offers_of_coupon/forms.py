from flask_wtf import FlaskForm
from wtforms import StringField, DecimalField, validators

class Betting_offer_of_couponForm(FlaskForm):
    choice_1x2 = StringField("Choice (1x2)", [validators.AnyOf(values=("1", "x", "2"))])

    class Meta:
        csrf = False
