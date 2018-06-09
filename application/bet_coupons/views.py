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

    return render_template("bet_coupons/new_bet_coupon.html", form = Bet_couponForm(), match_offer_tuples = match_offer_tuples)

@app.route("/bet_coupons/", methods=["POST"])
@login_required
def bet_coupons_create():
    offers = Betting_offer.query.all()
    offer_ids = []
    for offer in offers:
        id_candidate = request.form.get("hidden" + str(offer.id))
        if id_candidate != None:
            offer_ids.append(offer.id)

    form = Bet_couponForm(request.form)
    if not form.validate():
        match_offer_tuples = []
        for i in range(len(offer_ids)):
            if offer_ids[i] != None:
                offer = Betting_offer.query.get(offer_ids[i])
                match = Sport_match.query.get(offer.match_id)
                match_offer_tuples.append((match, offer))

        flash("Please, re-check your betting selections")
        return render_template("bet_coupons/new_bet_coupon.html", form = form, match_offer_tuples = match_offer_tuples)

    coupon = Bet_coupon()
    coupon.bettor_id = current_user.id
    db.session().add(coupon)
    db.session().commit()

    combined_odds = 1
    for offer_id in offer_ids:
        if offer_id != None:
            bo = Betting_offer.query.get(offer_id)
            choice = request.form.get(str(offer_id), "No bet")
            if  choice != "No bet":
                odds = bo.odds_for_choice(choice)
                combined_odds *= odds

                boc = Betting_offer_of_coupon(choice, odds)
                boc.bet_coupon_id = coupon.id
                boc.betting_offer_id = offer_id

                db.session().add(boc)
                db.session().commit()

    coupon.set_bet_details(combined_odds, form.stake_eur.data, form.stake_cent.data)
    db.session().commit()

    return redirect(url_for("bet_coupons_index"))

@app.route("/bet_coupons/show/<bet_coupon_id>", methods=["GET"])
@login_required
def bet_coupons_show(bet_coupon_id):
    coupon = Bet_coupon.query.get(bet_coupon_id)
    if coupon.bettor_id != current_user.id:
        flash("Please use the links provided to navigate the site")
        return redirect(url_for("bet_coupons_index"))

    offers_of_coupon = Betting_offer_of_coupon.query.filter_by(bet_coupon_id = bet_coupon_id).all()
    matches_offers_of_coupon = []
    for offer_of_coupon in offers_of_coupon:
        offer = Betting_offer.query.get(offer_of_coupon.betting_offer_id)
        match = Sport_match.query.get(offer.match_id)
        matches_offers_of_coupon.append((match, offer_of_coupon))

    return render_template("bet_coupons/show_bet_coupon.html", matches_offers_of_coupon = matches_offers_of_coupon, coupon = coupon)
