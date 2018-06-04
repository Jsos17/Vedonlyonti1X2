from flask import Flask
app = Flask(__name__)

from flask_sqlalchemy import SQLAlchemy
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///betting.db"
app.config["SQLALCHEMY_ECHO"] = True

db = SQLAlchemy(app)

from application import views

from application.matches import views
from application.matches import models
from application.betting_offers import views
from application.betting_offers import models
from application.bet_coupons import views
from application.bet_coupons import models
from application.betting_offers_of_coupon import views
from application.betting_offers_of_coupon import models
from application.auth import views
from application.auth import models

from application.auth.models import Bettor
from os import urandom
app.config["SECRET_KEY"] = urandom(32)

from flask_login import LoginManager
login_manager = LoginManager()
login_manager.init_app(app)

login_manager.login_view = "auth_login"
login_manager.login_message = "Please login to use this functionality."

@login_manager.user_loader
def load_user(user_id):
    return Bettor.query.get(user_id)

db.create_all()
