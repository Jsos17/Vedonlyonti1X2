from application import app, db, login_required
from flask import redirect, render_template, request, url_for, flash
from flask_login import current_user
from application.betting_offers.models import Betting_offer

@app.route("/statistics/turnover")
@login_required(role="ADMIN")
def turnover_index():
    return render_template("statistics/turnovers.html", results = Betting_offer.betting_offer_turnovers())

@app.route("/statistics/turnover/show/<home>/<away>/<offer_id>/")
@login_required(role="ADMIN")
def show_distribution(home, away, offer_id):
    return render_template("statistics/show_distribution.html", results = Betting_offer.choice_distribution(offer_id), home = home, away = away)
