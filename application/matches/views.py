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

@app.route("/matches/<match_id>/", methods=["POST"])
def matches_set_result(match_id):
    form = MatchForm(obj=Sport_match.query.get(match_id))
    return render_template("matches/update.html", form = form, match_id = match_id)

@app.route("/matches/update/<match_id>/", methods=["POST"])
def matches_update(match_id):
    form = MatchForm(request.form)
    if not form.validate():
        return render_template("matches/update.html", form = form, match_id = match_id)

    match = Sport_match.query.get(match_id)
    match.home = form.home.data
    match.away = form.away.data
    match.prob_1 = form.prob_1.data
    match.prob_x = form.prob_x.data
    match.prob_2 = form.prob_2.data
    match.start_time = form.start_time.data
    match.result_1x2 = form.result_1x2.data
    db.session().commit()

    return redirect(url_for("matches_index"))

@app.route("/matches/<match_id>/delete/", methods=["POST"])
def matches_delete(match_id):
    m = Sport_match.query.get(match_id)
    db.session().delete(m)
    db.session().commit()

    return redirect(url_for("matches_index"))

@app.route("/matches/", methods=["POST"])
def matches_create():
    form = MatchForm(request.form)

    if not form.validate():
        return render_template("matches/new.html", form = form)
    
    home = form.home.data
    away = form.away.data
    prob1 = form.prob_1.data
    probx = form.prob_x.data
    prob2 = form.prob_2.data
    start_time = form.start_time.data
    result_1x2 =form.result_1x2.data

    m = Sport_match(home, away, prob1, probx, prob2, start_time, result_1x2)

    db.session().add(m)
    db.session().commit()

    return redirect(url_for("matches_index"))