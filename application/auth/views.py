from flask import render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user

from application import app, db
from application.bet_coupons.models import Bet_coupon
from application.auth.models import Bettor
from application.auth.forms import LoginForm, BettorForm, UpdateUserForm

@app.route("/auth/login", methods= ["GET", "POST"])
def auth_login():
    if request.method == "GET":
        return render_template("auth/loginform.html", form = LoginForm())

    loginform = LoginForm(request.form)

    bettor = Bettor.query.filter_by(username=loginform.username.data, password=loginform.password.data).first()
    if not bettor:
        return render_template("auth/loginform.html", form = loginform, error="No such username or password")

    login_user(bettor)

    return redirect(url_for("index"))

@app.route("/auth/logout")
@login_required
def auth_logout():
    bets = Bet_coupon.query.filter_by(bettor_id = current_user.id, bet_status = "no bets").all()
    for bet in bets:
        db.session().delete(bet)
        db.session().commit()

    logout_user()
    return redirect(url_for("index"))

@app.route("/auth/new/")
def bettors_form():
    return render_template("auth/new_bettor.html", form = BettorForm())

@app.route("/auth/", methods=["POST"])
def bettor_create():
    form = BettorForm(request.form)

    if not form.validate():
        return render_template("auth/new_bettor.html", form = form)

    b = Bettor(form.username.data, form.password.data, form.balance_eur.data, form.balance_cent.data)
    db.session().add(b)
    db.session().commit()
    flash("Account created successfully, please login to your account")

    return redirect(url_for("auth_login"))

@app.route("/auth/show/", methods=["GET"])
@login_required
def bettor_show():
    return render_template("auth/show_user.html")

@app.route("/auth/cancel_update/", methods=["POST"])
@login_required
def bettor_cancel_update():
    return render_template("auth/show_user.html")

@app.route("/auth/update/", methods=["GET", "POST"])
@login_required
def bettor_update():
    if request.method == "POST":
        #form = BettorForm(request.form)
        form = UpdateUserForm(request.form)
        if not form.validate():
            return render_template("auth/update_user.html", form = form)

        b = Bettor.query.get(current_user.id)
        #b.username = form.username.data
        #b.password = form.password.data
        b.balance_eur = form.balance_eur.data
        b.balance_cent = form.balance_cent.data

        db.session().commit()
        flash("Account updated!")

        return redirect(url_for("bettor_show"))
    elif request.method == "GET":
        #form = BettorForm(obj=Bettor.query.get(id))
        form = UpdateUserForm()
        return render_template("auth/update_user.html", form = form)

@app.route("/auth/delete/", methods=["POST"])
@login_required
def bettor_delete():
    b = Bettor.query.get(current_user.id)
    db.session().delete(b)
    db.session().commit()
    flash("Account deleted successfully")

    return redirect(url_for("index"))
