from application import app, db
from flask import redirect, render_template, request, url_for
import datetime
from application.betting_offers.models import Betting_offer
from application.betting_offers.forms import Betting_offerForm

@app.route("/betting_offers", methods=["GET"])
def betting_offers_index():
    return render_template("betting_offers/offer_list.html", betting_offers = Betting_offer.query.all())

@app.route("/betting_offers/new/")
def betting_offers_form():


    return render_template("betting_offers/new_offer.html", form = Betting_offerForm())

@app.route("/betting_offers/", methods=["POST"])
def betting_offers_create():
    form = Betting_offerForm(request.form)

    if not form.validate():
        return render_template("betting_offers/new_offer.html", form = form)

    o1 = form.odds1.data
    ox = form.oddsx.data
    o2 = form.odds2.data
    ms = form.max_stake.data
    a = form.active.data
    c = form.closed.data

    bo = Betting_offer(o1, ox, o2, ms, a, c)

    db.session().add(bo)
    db.session().commit()

    return redirect(url_for("betting_offers_index"))