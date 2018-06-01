from application import db

class Bettor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(144), unique=True, nullable=False)
    password = db.Column(db.String(144), nullable=False)
    balance_eur = db.Column(db.Integer, nullable=False)
    balance_cent = db.Column(db.Integer, nullable=False)

    bets = db.relationship('Bet', backref='bettor', lazy=True)

    def __init__(self, username, password, balance_eur, balance_cent):
        self.username = username
        self.password = password
        self.balance_eur = balance_eur
        self.balance_cent = balance_cent

    def get_id(self):
        return self.id

    def is_active(self):
        return True
    
    def is_anonymous(self):
        return False

    def is_authenticated(self):
        return True