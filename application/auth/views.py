from flask import render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user

from application import app, db
from application.auth.models import Bettor
from application.auth.forms import LoginForm, BettorForm

@app.route("/auth/login", methods= ["GET", "POST"])
def auth_login():
    if request.method == "GET":
        return render_template("auth/loginform.html", form = LoginForm())

    loginform = LoginForm(request.form)

    bettor = Bettor.query.filter_by(username=loginform.username.data, password=loginform.password.data).first()
    if not bettor:
        return render_template("auth/loginform.html", form = loginform, error="No such username or password")

    login_user(bettor)
    print("User " + bettor.username + " was identified")

    return redirect(url_for("index"))

@app.route("/auth/logout")
def auth_logout():
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
    
    username = form.username.data
    password = form.password.data
    balance_eur = form.balance_eur.data
    balance_cent = form.balance_cent.data

    b = Bettor(username, password, balance_eur, balance_cent)

    db.session().add(b)
    db.session().commit()

    flash("Account created successfully, please login to your account")
    return redirect(url_for("auth_login"))
