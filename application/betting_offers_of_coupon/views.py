from application import app, db
from flask import redirect, render_template, request, url_for, flash
from flask_login import login_required, current_user
from application.auth.models import Bettor
from application.bet_coupons.models import Bet_coupon
from application.betting_offers.models import Betting_offer
from application.matches.models import Sport_match
from application.betting_offers_of_coupon.forms import Betting_offer_of_couponForm
from application.betting_offers_of_coupon.models import Betting_offer_of_coupon

@app.route("/betting_offers_of_coupon/<bet_coupon_id>", methods=["GET"])
@login_required
def betting_offers_of_coupon_index(bet_coupon_id):
    return render_template("betting_offers_of_coupon/betting_offers_of_coupon_list.html", bet_id = bet_id)

@app.route("/betting_offers_of_coupon/new/<betting_offer_id>/<bet_coupon_id>/", methods=["GET"])
@login_required
def betting_offers_of_coupon_form(betting_offer_id, bet_coupon_id):
    bo = Betting_offer.query.get(betting_offer_id)
    m = Sport_match.query.get(bo.match_id)
    return render_template("betting_offers_of_coupon/new_betting_offer_of_coupon.html", form = Betting_offer_of_couponForm(),
                betting_offer = bo, match = m)

# @app.route("/betting_offers_of_coupon/show/", methods=["GET"])
# @login_required
# def betting_offers_of_coupon_show():
#     return render_template("betting_offers_of_coupon/show_betting_offer_of_coupon.html")

@app.route("/betting_offers_of_coupon/<betting_offer_id>/<bet_coupon_id>/", methods=["POST"])
@login_required
def betting_offers_of_coupon_create(betting_offer_id, bet_coupon_id):
    form = Betting_offer_of_couponForm(request.form)
    bo = Betting_offer.query.get(betting_offer_id)
    if not form.validate():
        m = Sport_match.query.get(bo.match_id)
        return render_template("betting_offers_of_coupon/new_betting_offer_of_coupon.html", form = form,
                    betting_offer = bo, match = m)

    odds = bo.odds_for_choice(form.choice_1x2.data)

    boc = Betting_offer_of_coupon(form.choice_1x2.data, odds)
    boc.betting_offer_id = betting_offer_id
    boc.bet_id = bet_id

    db.session().add(boc)
    db.session().commit()

    return redirect(url_for("betting_offer_of_coupon_index"))
