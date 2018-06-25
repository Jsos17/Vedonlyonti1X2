from flask import Flask, flash
app = Flask(__name__)

from flask_sqlalchemy import SQLAlchemy
import os

if os.environ.get("HEROKU"):
    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL")
else:
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///betting.db"
    app.config["SQLALCHEMY_ECHO"] = True

db = SQLAlchemy(app)

from os import urandom
app.config["SECRET_KEY"] = urandom(32)
from flask_login import LoginManager, current_user
login_manager = LoginManager()
login_manager.init_app(app)

login_manager.login_view = "auth_login"
login_manager.login_message = "Please login to use this functionality."

from functools import wraps
def login_required(role="ANY"):
    def wrapper(fn):
        @wraps(fn)
        def decorated_view(*args, **kwargs):
            if current_user.is_authenticated():
                for bettor_role in current_user.roles():
                    if role == "ANY" or role == bettor_role:
                        return fn(*args, **kwargs)
                flash("You are not authorized to use this functionality")
                return login_manager.unauthorized()
            else:
                return login_manager.unauthorized()
        return decorated_view
    return wrapper

from application import views

from application.matches import views
from application.matches import models
from application.betting_offers import views
from application.betting_offers import models
from application.bet_coupons import views
from application.bet_coupons import models
from application.betting_offers_of_coupon import models
from application.roles import models
from application.user_roles import models
from application.auth import views
from application.auth import models
from application.statistics import views
from application.auth.models import Bettor
from application.roles.models import Role

@login_manager.user_loader
def load_user(user_id):
    return Bettor.query.get(user_id)

try:
    db.create_all()
except:
    pass

try:
    cust = Role.query.filter_by(name = "CUSTOMER").first()
    admin = Role.query.filter_by(name = "ADMIN").first()
    if cust == None:
        db.session().add(Role("CUSTOMER"))
    if admin == None:
        db.session().add(Role("ADMIN"))
    db.session().commit()
except:
    pass
