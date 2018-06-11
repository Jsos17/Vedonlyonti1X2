from application import db
from sqlalchemy.sql import text
from application.money_handler import sum_eur_cent, to_cents, distribution

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

    def odds_for_choice(self, choice):
        if choice == "1":
            return self.odds_1
        elif choice == "x":
            return self.odds_x
        elif choice == "2":
            return self.odds_2

    @staticmethod
    def betting_offer_turnovers():
        stmt = text("SELECT sport_match.home, sport_match.away, sport_match.id, betting_offer.id, \
                     COUNT(bet_coupon.id), SUM(bet_coupon.stake_eur), SUM(bet_coupon.stake_cent), sport_match.start_time \
                     FROM sport_match, betting_offer, bet_coupon, betting_offer_of_coupon WHERE betting_offer.match_id = sport_match.id \
                     AND betting_offer_of_coupon.betting_offer_id = betting_offer.id AND betting_offer_of_coupon.bet_coupon_id = bet_coupon.id GROUP BY sport_match.id, betting_offer.id")

        res = db.engine.execute(stmt)

        results = []
        for row in res:
            eur_cent = sum_eur_cent(row[5], row[6])
            results.append((row[0], row[1], row[2], row[3], row[4], eur_cent[0], eur_cent[1], row[7]))

        return results

    @staticmethod
    def choice_distribution(offer_id):
        stmt = text("SELECT sport_match.home, sport_match.away, COUNT(bet_coupon.id), betting_offer_of_coupon.choice_1x2, \
                     SUM(bet_coupon.stake_eur), SUM(bet_coupon.stake_cent), sport_match.prob_1, sport_match.prob_x, sport_match.prob_2 \
                     FROM sport_match, betting_offer, bet_coupon, betting_offer_of_coupon \
                     WHERE betting_offer_id = :offer_id AND betting_offer.match_id = sport_match.id \
                     AND betting_offer_of_coupon.betting_offer_id = betting_offer.id AND betting_offer_of_coupon.bet_coupon_id = bet_coupon.id \
                     GROUP BY sport_match.id, betting_offer_of_coupon.choice_1x2").params(offer_id = offer_id)

        res = db.engine.execute(stmt)

        d = {}
        probs = [0, 0, 0]
        cent_sum = 0
        for row in res:
            probs = [row[6], row[7], row[8]]
            cents = to_cents(row[4], row[5])
            cent_sum += cents
            d[row[3]] = [row[2], cents]

        if cent_sum == 0:
            return ("Nothing", 0, 0.0, 0, 0.00, 0)
        l = ["1", "x", "2"]
        results = []
        for i in range(3):
            choice = l[i]
            if choice not in d:
                results.append((choice, 0, 0.00, probs[i], 0.00, round(cent_sum/100, 2)))
            else:
                results.append((choice, d[choice][0], round(100*d[choice][1]/cent_sum, 2), probs[i], round(d[choice][1]/100, 2), round(cent_sum/100, 2)))

        return results
