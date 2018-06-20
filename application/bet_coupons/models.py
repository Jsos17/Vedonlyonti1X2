from application import db

class Bet_coupon(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    bettor_id = db.Column(db.Integer, db.ForeignKey('bettor.id'), nullable=False)
    combined_odds = db.Column(db.Float, nullable=False)
    stake_eur = db.Column(db.Integer, nullable=False)
    stake_cent = db.Column(db.Integer, nullable=False)
    possible_win_eur = db.Column(db.Integer, nullable=False)
    possible_win_cent = db.Column(db.Integer, nullable=False)
    bet_status = db.Column(db.String(10), nullable=False)

    def __init__(self):
        self.combined_odds = 1
        self.stake_eur = 0
        self.stake_cent = 0
        self.possible_win_eur = 0
        self.possible_win_cent = 0
        self.bet_status = "no bets"

    def calculate_win(self):
        money_in_cents = 100 * self.stake_eur + self.stake_cent
        win = int(round(self.combined_odds * money_in_cents, 0))
        self.possible_win_eur = win // 100
        self.possible_win_cent = win % 100

    def set_bet_details(self, combined_odds, stake_eur, stake_cent):
        self.combined_odds = round(combined_odds, 2)
        self.stake_eur = stake_eur
        self.stake_cent = stake_cent
        self.calculate_win()
        self.bet_status = "tbd"
