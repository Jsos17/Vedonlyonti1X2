from flask import render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from application import app, db
from application.bet_coupons.models import Bet_coupon
from application.auth.models import Bettor
from application.auth.forms import LoginForm, BettorForm, PasswordChangeForm, MoneyInForm, MoneyOutForm
from application.money_handler import to_cents, sum_eur_cent
from passlib.hash import sha256_crypt

@app.route("/auth/login", methods= ["GET", "POST"])
def auth_login():
    if request.method == "GET":
        return render_template("auth/loginform.html", form = LoginForm())

    loginform = LoginForm(request.form)
    # etsi käyttäjä nimellä, käyttäjänimet ovat uniikkeja
    bettor = Bettor.query.filter_by(username = loginform.username.data).first()
    # varmista, että annettu salasana on oikea
    if sha256_crypt.verify(loginform.password.data, bettor.password) == False:
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

    pw = sha256_crypt.encrypt(form.password.data)
    b = Bettor(form.username.data, pw, 0, 0)
    db.session().add(b)
    db.session().commit()
    flash("Account created successfully, please login to your account")
    flash("After you have logged in, you can transfer money to your account")

    return redirect(url_for("auth_login"))

@app.route("/auth/show/", methods=["GET"])
@login_required
def bettor_show():
    return render_template("auth/show_user.html")

@app.route("/auth/cancel_update/", methods=["POST"])
@login_required
def bettor_cancel_update():
    return render_template("auth/show_user.html")

@app.route("/auth/delete/", methods=["GET"])
@login_required
def bettor_delete():
    if current_user.role == "ADMIN":
        flash("Admin cannot delete account through the application")
        return render_template("auth/show_user.html")

    coupons = Bet_coupon.query.filter_by(bettor_id = current_user.id).all()
    for coupon in coupons:
        if coupon.bet_status == "tbd":
            flash("You have bets that are not determined yet")
            flash("You can delete your account when all your bets have been determined")
            return render_template("auth/show_user.html")

    return render_template("auth/delete_confirmation.html")

@app.route("/auth/delete/", methods=["POST"])
@login_required
def bettor_delete_confirmation():
    if current_user.role == "ADMIN":
        flash("Admin cannot delete account through the application")
        return render_template("auth/show_user.html")

    coupons = Bet_coupon.query.filter_by(bettor_id = current_user.id).all()
    b = Bettor.query.get(current_user.id)
    db.session().delete(b)
    db.session().commit()
    flash("Account deleted successfully")

    return redirect(url_for("index"))
@app.route("/auth/change_password", methods=["GET", "POST"])
@login_required
def bettor_change_password():
    if request.method == "GET":
        form = PasswordChangeForm()
        return render_template("auth/change_password.html", form = form)
    elif request.method == "POST":
        form = PasswordChangeForm(request.form)
        if not form.validate():
            return render_template("auth/change_password.html", form = form)

        b = Bettor.query.get(current_user.id)
        b.password = sha256_crypt.encrypt(form.new_password.data)
        db.session().commit()
        flash("Password changed successfully!")
        return render_template("auth/show_user.html")

@app.route("/auth/money_out", methods=["GET", "POST"])
@login_required
def bettor_transfer_out():
    if request.method == "GET":
        form = MoneyOutForm()
        return render_template("auth/money_out.html", form = form)
    elif request.method == "POST":
        form = MoneyOutForm(request.form)
        if not form.validate():
             return render_template("auth/money_out.html", form = form)

        b = Bettor.query.get(current_user.id)
        out_cents = int(100 * form.money_out.data)
        new_bal_cents = to_cents(b.balance_eur, b.balance_cent) - out_cents
        new_bal_eur_cent = sum_eur_cent(0, new_bal_cents)
        b.balance_eur = new_bal_eur_cent[0]
        b.balance_cent = new_bal_eur_cent[1]
        db.session().commit()
        flash("Money transferred successfully to your bank account")

        return render_template("auth/show_user.html")

@app.route("/auth/money_in", methods=["GET", "POST"])
@login_required
def bettor_transfer_in():
    if request.method == "GET":
        form = MoneyInForm()
        return render_template("auth/money_in.html", form = form)
    elif request.method == "POST":
        form = MoneyInForm(request.form)
        if not form.validate():
             return render_template("auth/money_in.html", form = form)

        b = Bettor.query.get(current_user.id)
        in_cents = int(100 * form.money_in.data)
        new_bal_cents = to_cents(b.balance_eur, b.balance_cent) + in_cents
        new_bal_eur_cent = sum_eur_cent(0, new_bal_cents)
        b.balance_eur = new_bal_eur_cent[0]
        b.balance_cent = new_bal_eur_cent[1]
        db.session().commit()
        flash("Money transferred successfully to your betting account")

        return render_template("auth/show_user.html")
