from application import db

class Match_result(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    match_id = db.Column(db.Integer, db.ForeignKey('sport_match.id'), nullable=False)
    result_1x2 = db.Column(db.String(1), nullable=False)

    def __init__(self, result_1x2):
        self.result_1x2 = result_1x2