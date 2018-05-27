from application import db

class Bettor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(144), nullable=False)
    password = db.Column(db.String(144), nullable=False)
    balance_eur = db.Column(db.Integer, nullable=False)
    balance_cent = db.Column(db.Integer, nullable=False)

    bets = db.relationship('Bet', backref='bettor', lazy=True)

    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.balance_eur = 0
        self.balance_cent = 0

    def get_id(self):
        return self.id
