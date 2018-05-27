from flask import Flask
app = Flask(__name__)

from flask_sqlalchemy import SQLAlchemy
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///betting.db"
app.config["SQLALCHEMY_ECHO"] = True

db = SQLAlchemy(app)

from application import views

from application.matches import models
from application.bettingoffers import models
from application.results import models
from application.bets import models
from application.bettingoffers_of_bet import models
from application.auth import models
from application.matches import views

db.create_all()
