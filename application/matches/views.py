from application import app, db
from flask import redirect, render_template, request, url_for
import datetime
from application.matches.models import Sport_match

@app.route("/matches", methods=["GET"])
def matches_index():
    return render_template("matches/list.html", matches = Sport_match.query.all())

@app.route("/matches/new/")
def matches_form():
    return render_template("matches/new.html")

@app.route("/matches/", methods=["POST"])
def matches_create():
    home = request.form.get("hometeam")
    away = request.form.get("awayteam")
    prob1 = request.form.get("prob_home")
    probx = request.form.get("prob_draw")
    prob2 = request.form.get("prob_away")    
    dt = datetime.datetime.strptime(request.form.get("date"), "%Y-%m-%d")
    tm = datetime.datetime.strptime(request.form.get("time"), "%H:%M")
    start_time = datetime.datetime.combine(dt.date(),tm.time())

    m = Sport_match(home, away, prob1, probx, prob2, start_time)

    db.session().add(m)
    db.session().commit()

    return redirect(url_for("matches_index"))