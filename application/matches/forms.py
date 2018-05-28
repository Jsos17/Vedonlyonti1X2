from flask_wtf import FlaskForm
from wtforms import (DateTimeField, IntegerField,
                     StringField, validators)

def validate_probabilities(form, field):
    p1 = form.prob1.data
    px = form.probx.data
    p2 = form.prob2.data
    try:
        if p1 + px + p2 != 100:
            raise validators.ValidationError("The sum of probabilities is not exactly 100 %")
    except TypeError:
        raise validators.ValidationError("Not a number")
    except ValueError:
        raise validators.ValidationError("Not a number")

class MatchForm(FlaskForm):
    home = StringField("Home team", [validators.InputRequired()])
    away = StringField("Away team", [validators.InputRequired()])
    prob1 = IntegerField("Home win probability (%)", [validators.NumberRange(min=0, max=100, message="Number between 0-100"), validate_probabilities])
    probx = IntegerField("Draw probability (%)", [validators.NumberRange(min=0, max=100, message="Number between 0-100"), validate_probabilities])
    prob2 = IntegerField("Away win probability (%)", [validators.NumberRange(min=0, max=100, message="Number between 0-100"), validate_probabilities])
    start_time = DateTimeField("Starting time (YYYY-mm-dd HH:MM)", format='%Y-%m-%d %H:%M')
 
    class Meta:
        csrf = False
