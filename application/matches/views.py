from application import app, db
from flask import redirect, render_template, request, url_for
import datetime
from application.matches.models import Sport_match
from application.matches.forms import MatchForm

@app.route("/matches", methods=["GET"])
def matches_index():
    return render_template("matches/list.html", matches = Sport_match.query.all())

@app.route("/matches/new/")
def matches_form():
    return render_template("matches/new.html", form = MatchForm())

@app.route("/matches/", methods=["POST"])
def matches_create():
    form = MatchForm(request.form)

    if not form.validate():
        return render_template("matches/new.html", form = form)
    
    home = form.home.data
    away = form.away.data
    prob1 = form.prob1.data
    probx = form.probx.data
    prob2 = form.prob2.data
    start_time = form.start_time.data

    m = Sport_match(home, away, prob1/100, probx/100, prob2/100, start_time)

    db.session().add(m)
    db.session().commit()

    return redirect(url_for("matches_index"))