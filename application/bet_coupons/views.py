from application import app, db
from flask import redirect, render_template, request, url_for, flash
from flask_login import login_required, current_user
from application.auth.models import Bettor
from application.matches.models import Sport_match
from application.betting_offers.models import Betting_offer
from application.bet_coupons.models import Bet_coupon
from application.bet_coupons.forms import Bet_couponForm
from application.betting_offers_of_coupon.models import Betting_offer_of_coupon
from application.money_handler import sum_eur_cent, to_cents

@app.route("/bet_coupons/")
@login_required
def bet_coupons_index():
    if (current_user.role == "ADMIN"):
        flash("Administrator cannot place bets")
        return render_template("index.html")

    bet_coupons = Bet_coupon.query.filter_by(bettor_id = current_user.id).all()
    return render_template("bet_coupons/bet_coupon_list.html", user_coupons = bet_coupons)

@app.route("/bet_coupons/new/", methods=["POST"])
@login_required
def bet_coupons_form():
    if (current_user.role == "ADMIN"):
        flash("Administrator cannot place bets")
        return render_template("index.html")

    offers = Betting_offer.query.all()
    match_offer_tuples = []
    maximum_stake = 100
    for offer in offers:
        if request.form.get(str(offer.id), "Remove") == "Add":
            match = Sport_match.query.get(offer.match_id)
            match_offer_tuples.append((match, offer))

            if offer.max_stake < maximum_stake:
                maximum_stake = offer.max_stake

    if len(match_offer_tuples) == 0:
        flash("Add at least one betting offer to coupon")
        return redirect(url_for("betting_offers_index"))

    return render_template("bet_coupons/new_bet_coupon.html", form = Bet_couponForm(), match_offer_tuples = match_offer_tuples, max_stake = maximum_stake)

@app.route("/bet_coupons/", methods=["POST"])
@login_required
def bet_coupons_create():
    if (current_user.role == "ADMIN"):
        flash("Administrator cannot place bets")
        return render_template("index.html")

    offers = Betting_offer.query.all()
    offer_ids = []
    for offer in offers:
        id_candidate = request.form.get("hidden" + str(offer.id))
        if id_candidate != None:
            offer_ids.append(offer.id)

    form = Bet_couponForm(request.form)
    if not form.validate():
        match_offer_tuples = []
        maximum_stake = 100
        for i in range(len(offer_ids)):
            if offer_ids[i] != None:
                offer = Betting_offer.query.get(offer_ids[i])
                match = Sport_match.query.get(offer.match_id)
                match_offer_tuples.append((match, offer))

                if offer.max_stake < maximum_stake:
                    maximum_stake = offer.max_stake

        flash("Please, re-check your betting selections")
        return render_template("bet_coupons/new_bet_coupon.html", form = form, match_offer_tuples = match_offer_tuples, max_stake = maximum_stake)

    coupon = Bet_coupon()
    coupon.bettor_id = current_user.id
    db.session().add(coupon)
    # commit tyhjä coupon jotta sen id saadaan tietoon
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

    coupon.set_bet_details(combined_odds, form.stake_eur.data, form.stake_cent.data)

    # subtract stake from bettor's balance
    stake_cents = to_cents(form.stake_eur.data, form.stake_cent.data)
    balance_cents= to_cents(current_user.balance_eur, current_user.balance_cent)
    new_balance = sum_eur_cent(0, balance_cents - stake_cents)

    b = Bettor.query.get(current_user.id)
    b.balance_eur = new_balance[0]
    b.balance_cent = new_balance[1]

    # commit kaikkien Betting_offer_of_coupongien lisäys, Bet_couponin ja Bettorin päivitys
    db.session().commit()

    return redirect(url_for("bet_coupons_index"))

@app.route("/bet_coupons/show/<bet_coupon_id>", methods=["GET"])
@login_required
def bet_coupons_show(bet_coupon_id):
    if (current_user.role == "ADMIN"):
        flash("Administrator cannot place bets")
        return render_template("index.html")

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
