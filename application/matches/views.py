from application import app, db
from flask import redirect, render_template, request, url_for, flash
from flask_login import login_required, current_user
import datetime
from application.matches.models import Sport_match
from application.betting_offers.models import Betting_offer
from application.matches.forms import MatchForm, SetResultForm

@app.route("/matches", methods=["GET"])
@login_required
def matches_index():
    if (current_user.role != "ADMIN"):
        flash("Please use the provided links")
        return render_template("index.html")

    return render_template("matches/list.html", matches = Sport_match.query.all())

@app.route("/matches/new/")
@login_required
def matches_form():
    if (current_user.role != "ADMIN"):
        flash("Please use the provided links")
        return render_template("index.html")

    return render_template("matches/new.html", form = MatchForm())

@app.route("/matches/show/<match_id>", methods=["GET"])
@login_required
def matches_show(match_id):
    if (current_user.role != "ADMIN"):
        flash("Please use the provided links")
        return render_template("index.html")

    return render_template("matches/show_match.html", match = Sport_match.query.get(match_id))

@app.route("/matches/update/<match_id>/", methods=["GET", "POST"])
@login_required
def matches_update(match_id):
    if (current_user.role != "ADMIN"):
        flash("Please use the provided links")
        return render_template("index.html")

    if request.method == "POST":
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
        db.session().commit()

        return redirect(url_for("matches_show", match_id = match_id))
    elif request.method == "GET":
        form = MatchForm(obj=Sport_match.query.get(match_id))
        return render_template("matches/update.html", form = form, match_id = match_id)

@app.route("/matches/set_result/<match_id>/", methods=["GET", "POST"])
@login_required
def matches_set_result(match_id):
    if (current_user.role != "ADMIN"):
        flash("Please use the provided links")
        return render_template("index.html")
    m = Sport_match.query.get(match_id)
    old_result = m.result_1x2
    if request.method == "POST":
        form = SetResultForm(request.form)
        if not form.validate():
            return render_template("matches/set_result.html", form = form, match_id = match_id, old_result = old_result)

        match = Sport_match.query.get(match_id)
        old_result = match.result_1x2
        if old_result == "tbd":
            match.result_1x2 = form.result_1x2.data
            db.session().commit()

        return redirect(url_for("matches_show", match_id = match_id))
    elif request.method == "GET":
        form = SetResultForm()
        return render_template("matches/set_result.html", form = form, match_id = match_id, old_result = old_result)

@app.route("/matches/<match_id>/delete/", methods=["POST"])
@login_required
def matches_delete(match_id):
    if (current_user.role != "ADMIN"):
        flash("Please use the provided links")
        return render_template("index.html")

    bo = Betting_offer.query.filter_by(match_id = match_id).first()
    if bo == None:
        m = Sport_match.query.get(match_id)
        db.session().delete(m)
        db.session().commit()

        return redirect(url_for("matches_index"))
    else:
        flash("There are betting offers related to the match, deletion denied")
        return redirect(url_for("matches_show", match_id = match_id))

@app.route("/matches/", methods=["POST"])
@login_required
def matches_create():
    if (current_user.role != "ADMIN"):
        flash("Please use the provided links")
        return render_template("index.html")

    form = MatchForm(request.form)
    if not form.validate():
        return render_template("matches/new.html", form = form)

    m = Sport_match(form.home.data, form.away.data, form.prob_1.data, form.prob_x.data,
                    form.prob_2.data, form.start_time.data)

    db.session().add(m)
    db.session().commit()

    return redirect(url_for("matches_index"))
