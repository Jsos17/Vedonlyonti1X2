from application import db

class Betting_offer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    match_id = db.Column(db.Integer, db.ForeignKey('sport_match.id'), nullable=False)
    odds_1 = db.Column(db.Float, nullable=False)
    odds_x = db.Column(db.Float, nullable=False)
    odds_2 = db.Column(db.Float, nullable=False)
    max_stake = db.Column(db.Float, nullable=False)
    active = db.Column(db.Boolean, nullable=False)
    closed = db.Column(db.Boolean, nullable=False)

    def __init__(self, odds_1, odds_x, odds_2, max_stake, active, closed):
        self.odds_1 = odds_1
        self.odds_x = odds_x
        self.odds_2 = odds_2
        self.max_stake = max_stake
        self.active = active
        self.closed = closed
