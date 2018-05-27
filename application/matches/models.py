from application import db

class Sport_match(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    home = db.Column(db.String(144), nullable=False)
    away = db.Column(db.String(144), nullable=False)
    prob_1 = db.Column(db.Float, nullable=False)
    prob_x = db.Column(db.Float, nullable=False)
    prob_2 = db.Column(db.Float, nullable=False)
    time = db.Column(db.DateTime, nullable=False)

    betoffer = db.relationship('Betting_offer', backref='sport_match', lazy=True)
    result = db.relationship('Match_result', backref='sport_match', lazy=True)

    def __init__(self, home, away, prob_1, prob_x, prob_2, time):
        self.home = home
        self.away = away
        self.prob_1 = prob_1
        self.prob_x = prob_x
        self.prob_2 = prob_2
        self.time = time
