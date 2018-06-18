from application import app, db
from flask import redirect, render_template, request, url_for, flash
from flask_login import login_required, current_user
from application.auth.models import Bettor
from application.matches.models import Sport_match
from application.betting_offers.models import Betting_offer
from application.bet_coupons.models import Bet_coupon
from application.bet_coupons.forms import Bet_couponForm
from application.betting_offers_of_coupon.models import Betting_offer_of_coupon
from application import money_handler

@app.route("/statistics/turnover")
def turnover_index():
    return render_template("statistics/turnovers.html", results = Betting_offer.betting_offer_turnovers())

@app.route("/statistics/turnover/show/<home>/<away>/<offer_id>/")
def show_distribution(home, away, offer_id):
    return render_template("statistics/show_distribution.html", results = Betting_offer.choice_distribution(offer_id), home = home, away = away)
