from application import app, db, login_required
from flask import redirect, render_template, request, url_for, flash
from flask_login import current_user
import datetime
from application.matches.models import Sport_match
from application.betting_offers.models import Betting_offer
from application.betting_offers_of_coupon.models import Betting_offer_of_coupon
from application.bet_coupons.models import Bet_coupon
from application.auth.models import Bettor
from application.matches.forms import MatchForm, SetResultForm
from application.money_handler import sum_eur_cent, to_cents

@app.route("/matches", methods=["GET"])
@login_required(role="ADMIN")
def matches_index():
    return render_template("matches/list.html", matches = Sport_match.query.all())

@app.route("/matches/new/")
@login_required(role="ADMIN")
def matches_form():
    return render_template("matches/new.html", form = MatchForm())

@app.route("/matches/show/<match_id>", methods=["GET"])
@login_required(role="ADMIN")
def matches_show(match_id):
    return render_template("matches/show_match.html", match = Sport_match.query.get(match_id),
                           betting_offer = Betting_offer.query.filter_by(match_id = match_id).first())

@app.route("/matches/update/<match_id>/", methods=["GET", "POST"])
@login_required(role="ADMIN")
def matches_update(match_id):
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
@login_required(role="ADMIN")
def matches_set_result(match_id):
    m = Sport_match.query.get(match_id)
    old_result = m.result_1x2
    if request.method == "POST":
        form = SetResultForm(request.form)

        if not form.validate():
            return render_template("matches/set_result.html", form = form, match_id = match_id, old_result = old_result)

        # tulos -> kuponkien kohteiden valinnan vertailu tulokseen -> mahdollinen voitonjako pelaajille
        match = Sport_match.query.get(match_id)
        old_result = match.result_1x2
        if old_result == "tbd":
            res = form.result_1x2.data
            match.result_1x2 = res
            offer = Betting_offer.query.filter_by(match_id=match.id).first()
            if offer != None:
                offer.active = False
                offer.closed  = True
                offers_of_coupons = Betting_offer_of_coupon.query.filter_by(betting_offer_id = offer.id).all()
                for offer_of_coupon in offers_of_coupons:
                    coupon = Bet_coupon.query.get(offer_of_coupon.bet_coupon_id)

                    if offer_of_coupon.choice_1x2 == res:
                        offer_of_coupon.status = "hit"
                        if coupon.bet_status == "tbd":
                            offers_of_this_coupon = Betting_offer_of_coupon.query.filter_by(bet_coupon_id = coupon.id).all()
                            count = len(offers_of_this_coupon)
                            i = 0
                            while i < count:
                                if offers_of_this_coupon[i].status == "hit":
                                    i += 1
                                else:
                                    if offers_of_this_coupon[i].status == "miss":
                                        coupon.bet_status = "loss"
                                    break
                            # voitonmaksu
                            if i == count:
                                coupon.bet_status = "win"
                                b = Bettor.query.get(coupon.bettor_id)
                                new_balance = sum_eur_cent(b.balance_eur + coupon.possible_win_eur, b.balance_cent + coupon.possible_win_cent)
                                b.balance_eur = new_balance[0]
                                b.balance_cent = new_balance[1]
                    # panos palautetaan
                    elif res == "void":
                        offer_of_coupon.status = "nil"
                        coupon.bet_status = "void"
                        b = Bettor.query.get(coupon.bettor_id)
                        new_balance = sum_eur_cent(b.balance_eur + coupon.stake_eur, b.balance_cent + coupon.stake_cent)
                        b.balance_eur = new_balance[0]
                        b.balance_cent = new_balance[1]
                    else:
                        offer_of_coupon.status = "miss"
                        coupon.bet_status = "loss"

            db.session().commit()

        return redirect(url_for("matches_show", match_id = match_id))
    elif request.method == "GET":
        form = SetResultForm()
        return render_template("matches/set_result.html", form = form, match_id = match_id, old_result = old_result)

@app.route("/matches/<match_id>/delete/", methods=["POST"])
@login_required(role="ADMIN")
def matches_delete(match_id):
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
@login_required(role="ADMIN")
def matches_create():
    form = MatchForm(request.form)
    if not form.validate():
        return render_template("matches/new.html", form = form)

    m = Sport_match(form.home.data, form.away.data, form.prob_1.data, form.prob_x.data,
                    form.prob_2.data, form.start_time.data)

    db.session().add(m)
    db.session().commit()

    return redirect(url_for("matches_index"))
