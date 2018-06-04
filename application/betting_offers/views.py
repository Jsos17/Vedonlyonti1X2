from application import app, db
from flask import redirect, render_template, request, url_for, flash
import datetime
from application.matches.models import Sport_match
from application.matches import views
from application.betting_offers.models import Betting_offer
from application.betting_offers.forms import Betting_offerForm
from application.betting_offers.bookmaker import Handicapper

@app.route("/betting_offers", methods=["GET"])
def betting_offers_index():
    offers = Betting_offer.query.all()
    match_offer_tuples = []
    for offer in offers:
        match = Sport_match.query.get(offer.match_id)
        match_offer_tuples.append((match, offer))
    return render_template("betting_offers/offer_list.html", match_offer_tuples = match_offer_tuples)

@app.route("/betting_offers/new/<match_id>", methods=["GET"])
def betting_offers_form(match_id):
    bo = Betting_offer.query.filter_by(match_id = match_id).first()
    if bo == None:
        m = Sport_match.query.get(match_id)
        h = Handicapper(89.5)
        odds = h.handicap(m.prob_1, m.prob_x, m.prob_2)
        bo = Betting_offer(odds[0], odds[1], odds[2], 100, True, False)
        return render_template("betting_offers/new_offer.html", form = Betting_offerForm(obj=bo), match_id = match_id, home = m.home, away = m.away)
    else:
        flash("Betting offer exists already")
        return redirect(url_for("matches_show", match_id = match_id))


@app.route("/betting_offers/<match_id>", methods=["POST"])
def betting_offers_create(match_id):
    form = Betting_offerForm(request.form)
    if not form.validate():
        m = Sport_match.query.get(match_id)
        return render_template("betting_offers/new_offer.html", form = form, match_id = match_id,  home = m.home, away = m.away)

    offer = Betting_offer(form.odds_1.data, form.odds_x.data, form.odds_2.data,
            form.max_stake.data, form.active.data, form.closed.data)
    offer.match_id = match_id

    db.session().add(offer)
    db.session().commit()

    return redirect(url_for("betting_offers_index"))
