from application import db

class Sport_match(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    home = db.Column(db.String(144), nullable=False)
    away = db.Column(db.String(144), nullable=False)
    prob_1 = db.Column(db.Integer, nullable=False)
    prob_x = db.Column(db.Integer, nullable=False)
    prob_2 = db.Column(db.Integer, nullable=False)
    start_time = db.Column(db.DateTime, nullable=False)
    result_1x2 = db.Column(db.String(4), nullable=False)

    betoffer = db.relationship('Betting_offer', backref='sport_match', lazy=True, uselist=False)

    def __init__(self, home, away, prob_1, prob_x, prob_2, start_time, result_1x2):
        self.home = home
        self.away = away
        self.prob_1 = prob_1
        self.prob_x = prob_x
        self.prob_2 = prob_2
        self.start_time = start_time
        self.result_1x2 = result_1x2

    def get_id(self):
        return self.id
