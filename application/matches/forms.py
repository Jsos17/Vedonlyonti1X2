from flask_wtf import FlaskForm
from wtforms import Form, DateTimeField, IntegerField, StringField, validators

def validate_probabilities(form, field):
    try:
        p1 = int(form.prob1.data)
        px = int(form.probx.data)
        p2 = int(form.prob2.data)

        if p1 + px + p2 != 100:
            raise validators.ValidationError("The sum of probabilities is not exactly 100 %")
    except TypeError:
        raise validators.ValidationError()
    
class MatchForm(FlaskForm):
    home = StringField("Home team", [validators.InputRequired()])
    away = StringField("Away team", [validators.InputRequired()])
    prob1 = IntegerField("Home win probability (integer value 0-100 %)", [validators.NumberRange(min=0, max=100), validate_probabilities])
    probx = IntegerField("Draw probability (integer value 0-100 %)", [validators.NumberRange(min=0, max=100), validate_probabilities])
    prob2 = IntegerField("Away win probability (integer value 0-100 %)", [validators.NumberRange(min=0, max=100), validate_probabilities])
    start_time = DateTimeField("Starting time (format: YYYY-mm-dd HH:MM)", format='%Y-%m-%d %H:%M')
 
    class Meta:
        csrf = False
