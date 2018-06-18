from application import app, db
from flask import redirect, render_template, request, url_for, flash
from flask_login import login_required, current_user
import datetime
from application.matches.models import Sport_match
from application.matches import views
from application.betting_offers.models import Betting_offer
from application.betting_offers.forms import Betting_offerForm
from application.betting_offers.bookmaker import Handicapper
from application.betting_offers_of_coupon.models import Betting_offer_of_coupon

@app.route("/betting_offers", methods=["GET"])
def betting_offers_index():
    offers = Betting_offer.query.filter_by(active=True, closed=False).all()
    match_offer_tuples = []
    for offer in offers:
        match = Sport_match.query.get(offer.match_id)
        match_offer_tuples.append((match, offer))
    return render_template("betting_offers/offer_list.html", match_offer_tuples = match_offer_tuples)

@app.route("/betting_offers/admin", methods=["GET"])
@login_required
def admin_betting_offers_index():
    if (current_user.role != "ADMIN"):
        flash("Please use the provided links")
        return render_template("index.html")

    offers = Betting_offer.query.all()
    match_offer_tuples = []
    for offer in offers:
        match = Sport_match.query.get(offer.match_id)
        match_offer_tuples.append((match, offer))
    return render_template("betting_offers/admin_offer_list.html", match_offer_tuples = match_offer_tuples)

@app.route("/betting_offers/new/<match_id>", methods=["GET"])
@login_required
def betting_offers_form(match_id):
    if (current_user.role != "ADMIN"):
        flash("Please use the provided links")
        return render_template("index.html")

    bo = Betting_offer.query.filter_by(match_id = match_id).first()
    if bo == None:
        m = Sport_match.query.get(match_id)
        if m.result_1x2 != "tbd":
            flash("Match result is already determined or voided, betting offer cannot be created")
            return redirect(url_for("matches_show", match_id = match_id))

        h = Handicapper(89.5)
        odds = h.handicap(m.prob_1, m.prob_x, m.prob_2)
        bo = Betting_offer(odds[0], odds[1], odds[2], 100, True, False)
        return render_template("betting_offers/new_offer.html", form = Betting_offerForm(obj=bo), match = m)
    else:
        flash("Betting offer exists already")
        return redirect(url_for("matches_show", match_id = match_id))

@app.route("/betting_offers/<match_id>", methods=["POST"])
@login_required
def betting_offers_create(match_id):
    if (current_user.role != "ADMIN"):
        flash("Please use the provided links")
        return render_template("index.html")

    form = Betting_offerForm(request.form)
    if not form.validate():
        m = Sport_match.query.get(match_id)
        return render_template("betting_offers/new_offer.html", form = form, match = m)

    offer = Betting_offer(form.odds_1.data, form.odds_x.data, form.odds_2.data,
                          form.max_stake.data, form.active.data, form.closed.data)
    offer.match_id = match_id

    db.session().add(offer)
    db.session().commit()

    return redirect(url_for("admin_betting_offers_index"))

@app.route("/betting_offers/update/<offer_id>", methods=["GET", "POST"])
@login_required
def betting_offers_update(offer_id):
    if (current_user.role != "ADMIN"):
        flash("Please use the provided links")
        return render_template("index.html")

    if request.method == "GET":
        bo = Betting_offer.query.get(offer_id)
        m = Sport_match.query.get(bo.match_id)
        form = Betting_offerForm(obj=bo)
        return render_template("betting_offers/update_offer.html", offer_id = offer_id, form = form, match = m)
    elif request.method == "POST":
        form = Betting_offerForm(request.form)
        bo = Betting_offer.query.get(offer_id)
        if not form.validate():
            m = Sport_match.query.get(bo.match_id)
            return render_template("betting_offers/update_offer.html", offer_id = offer_id, form = form, match = m)

        bo.odds_1 = form.odds_1.data
        bo.odds_x = form.odds_x.data
        bo.odds_2 = form.odds_2.data
        bo.max_stake = form.max_stake.data
        bo.active = form.active.data
        bo.closed = form.closed.data

        db.session().commit()
        return redirect(url_for("admin_betting_offers_index"))

@app.route("/betting_offers/delete/<offer_id>", methods=["POST"])
@login_required
def betting_offers_delete(offer_id):
    if (current_user.role != "ADMIN"):
        flash("Please use the provided links")
        return render_template("index.html")

    bofc = Betting_offer_of_coupon.query.filter_by(betting_offer_id = offer_id).all()
    bo = Betting_offer.query.get(offer_id)

    if len(bofc) > 0:
        flash("Bets have been placed on this offer, deletion denied")
    elif bo.active == True:
        flash("Make the offer inactive, then proceed to delete it")
        m = Sport_match.query.get(bo.match_id)
        form = Betting_offerForm(obj=bo)
        return render_template("betting_offers/update_offer.html", offer_id = offer_id, form = form, match = m)
    else:
        db.session().delete(bo)
        db.session().commit()
        flash("Betting offer deleted")

    return redirect(url_for("admin_betting_offers_index"))
