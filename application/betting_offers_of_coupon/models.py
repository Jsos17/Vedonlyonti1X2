from application import db

class Betting_offer_of_coupon(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    betting_offer_id = db.Column(db.Integer, db.ForeignKey('betting_offer.id'), nullable=False)
    bet_coupon_id = db.Column(db.Integer, db.ForeignKey('bet_coupon.id'), nullable=False)
    choice_1x2 = db.Column(db.String(1), nullable=False)
    odds = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(10), nullable=False)

    def __init__(self, choice_1x2, odds):
        self.choice_1x2 = choice_1x2
        self.odds = odds
        self.status = "tbd"
