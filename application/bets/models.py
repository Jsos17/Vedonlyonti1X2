from application import db

class Bet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    bettor_id = db.Column(db.Integer, db.ForeignKey('bettor.id'), nullable=False)
    combined_odds = db.Column(db.Float, nullable=False)
    stake_eur = db.Column(db.Integer, nullable=False)
    stake_cent = db.Column(db.Integer, nullable=False)
    possible_win_eur = db.Column(db.Integer, nullable=False)
    possible_win_cent = db.Column(db.Integer, nullable=False)
    bet_status = db.Column(db.String(10), nullable=False)

    def __init__(self, combined_odds, stake_eur, stake_cent):
        self.combined_odds = combined_odds
        self.stake_eur = stake_eur
        self.stake_cent = stake_cent
        self.possible_win_eur = 0
        self.possible_win_cent = 0
        self.bet_status = "TBD"