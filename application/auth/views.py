from flask import render_template, request, redirect, url_for
from flask_login import login_user, logout_user

from application import app
from application.auth.models import Bettor
from application.auth.forms import LoginForm

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
