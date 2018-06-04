from application import app, db
from flask import redirect, render_template, request, url_for, flash
from flask_login import login_required, current_user
from application.auth.models import Bettor
from application.matches.models import Sport_match
from application.betting_offers.models import Betting_offer
from application.bet_coupons.models import Bet_coupon
from application.bet_coupons.forms import Bet_couponForm
from application.betting_offers_of_coupon.models import Betting_offer_of_coupon

@app.route("/bet_coupons/")
@login_required
def bet_coupons_index():
    bet_coupons = Bet_coupon.query.filter_by(bettor_id = current_user.id).all()
    return render_template("bet_coupons/bet_coupon_list.html", user_coupons = bet_coupons)

@app.route("/bet_coupons/new/", methods=["POST"])
@login_required
def bet_coupons_form():
    offers = Betting_offer.query.all()
    match_offer_tuples = []
    for offer in offers:
        if request.form.get(str(offer.id), "Remove") == "Add":
            match = Sport_match.query.get(offer.match_id)
            match_offer_tuples.append((match, offer))

    if len(match_offer_tuples) != 1:
        flash("Add  exactly one betting offer to coupon")
        return redirect(url_for("betting_offers_index"))

    return render_template("bet_coupons/new_bet_coupon.html", form = Bet_couponForm(), match_offer_tuples = match_offer_tuples)

@app.route("/bet_coupons/show/", methods=["GET"])
@login_required
def bet_coupons_show():
    return render_template("bet_coupons/show_bet_coupon.html", bet_coupons = Bet_coupon.query.get(bettor_id = current_user.id).all())

@app.route("/bet_coupons/<betting_offer_id>", methods=["POST"])
@login_required
def bet_coupons_create(betting_offer_id):
    form = Bet_couponForm(request.form)
    if not form.validate():
        return render_template("bet_coupons/new_bet_coupon.html", form = form)

    b = Bet_coupon()
    b.bettor_id = current_user.id
    db.session().add(b)
    db.session().commit()

    choice = form.choice_1x2.data
    bo = Betting_offer.query.get(betting_offer_id)
    odds = bo.odds_for_choice(choice)

    boc = Betting_offer_of_coupon(choice, odds)
    boc.bet_coupon_id = b.id
    boc.betting_offer_id = betting_offer_id

    db.session().add(boc)
    db.session().commit()

    b.set_bet_details(odds, form.stake_eur.data, form.stake_cent.data)
    db.session().commit()

    return redirect(url_for("bet_coupons_index"))
