from flask_wtf import FlaskForm
from wtforms import DateTimeField, IntegerField, StringField, validators

def validate_probabilities(form, field):
    try:
        p1 = int(form.prob_1.data)
        px = int(form.prob_x.data)
        p2 = int(form.prob_2.data)

        if p1 + px + p2 != 100:
            raise validators.ValidationError("The sum of probabilities is not exactly 100 %")
    except TypeError:
        raise validators.ValidationError()

class MatchForm(FlaskForm):
    home = StringField("Home team", [validators.InputRequired()])
    away = StringField("Away team", [validators.InputRequired()])
    prob_1 = IntegerField("Home win probability (integer value 1-100 %)", [validators.NumberRange(min=1, max=100), validate_probabilities])
    prob_x = IntegerField("Draw probability (integer value 1-100 %)", [validators.NumberRange(min=1, max=100), validate_probabilities])
    prob_2 = IntegerField("Away win probability (integer value 1-100 %)", [validators.NumberRange(min=1, max=100), validate_probabilities])
    start_time = DateTimeField("Starting time (format: YYYY-mm-dd HH:MM)", format='%Y-%m-%d %H:%M')
    result_1x2 = StringField("Result (tbd, void, 1, x, 2)", [validators.AnyOf(values=("tbd", "void", "1", "x", "2"))])

    class Meta:
        csrf = False
