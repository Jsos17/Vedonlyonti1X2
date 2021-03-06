from application import app, db, login_required
from flask import redirect, render_template, request, url_for, flash
from flask_login import current_user
from application.auth.models import Bettor
from application.matches.models import Sport_match
from application.betting_offers.models import Betting_offer
from application.bet_coupons.models import Bet_coupon
from application.bet_coupons.forms import Bet_couponForm
from application.betting_offers_of_coupon.models import Betting_offer_of_coupon
from application.money_handler import sum_eur_cent, to_cents

@app.route("/bet_coupons/")
@login_required(role="CUSTOMER")
def bet_coupons_index():
    coupons = Bet_coupon.query.filter_by(bettor_id = current_user.id).all()
    stakes_cent_total = 0
    wins_cent_total = 0
    pending = 0
    for coupon in coupons:
        stakes_cent_total += to_cents(coupon.stake_eur, coupon.stake_cent)
        if coupon.bet_status == "win":
            wins_cent_total += to_cents(coupon.possible_win_eur, coupon.possible_win_cent)
        elif coupon.bet_status == "void":
            wins_cent_total += to_cents(coupon.stake_eur, coupon.stake_cent)
        elif coupon.bet_status == "tbd":
            pending += 1

    profit_cents = wins_cent_total - stakes_cent_total
    profit = round(profit_cents / 100, 2)
    winnings = sum_eur_cent(0, wins_cent_total)
    stakes = sum_eur_cent(0, stakes_cent_total)
    tuple_list = [winnings, stakes]

    coupon_count = len(coupons)
    determined = coupon_count - pending

    return render_template("bet_coupons/bettor_history.html", tuple_list = tuple_list, profit = profit,
                           coupon_count = coupon_count, pending = pending, determined = determined, user_coupons = coupons)

@app.route("/bet_coupons/new/", methods=["POST"])
@login_required(role="CUSTOMER")
def bet_coupons_form():
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
@login_required(role="CUSTOMER")
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

    # extra check for balance
    stake_cents = int(100 * form.stake.data)
    balance_cents = to_cents(current_user.balance_eur, current_user.balance_cent)
    if stake_cents > balance_cents:
        flash("Your stake exceeds your balance")
        return redirect(url_for("bet_coupons_index"))

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

    stake_eur_cent = sum_eur_cent(0, stake_cents)
    coupon.set_bet_details(combined_odds, stake_eur_cent[0], stake_eur_cent[1])

    # subtract stake from bettor's balance
    new_balance = sum_eur_cent(0, balance_cents - stake_cents)

    b = Bettor.query.get(current_user.id)
    b.balance_eur = new_balance[0]
    b.balance_cent = new_balance[1]

    # commit kaikkien Betting_offer_of_coupongien lisäys, Bet_couponin ja Bettorin päivitys
    db.session().commit()

    return redirect(url_for("bet_coupons_index"))

@app.route("/bet_coupons/show/<bet_coupon_id>", methods=["GET"])
@login_required(role="CUSTOMER")
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
