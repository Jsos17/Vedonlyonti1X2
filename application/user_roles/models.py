from application import db

class User_role(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    bettor_id = db.Column(db.Integer, db.ForeignKey('bettor.id'), nullable=False)
    role_id = db.Column(db.Integer, db.ForeignKey('role.id'), nullable=False)

    def __init__(self):
        pass
