from application import db

class Role(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(10), unique=True, nullable=False)

    user_roles = db.relationship('User_role', cascade="delete", backref='role', lazy=True)

    def __init__(self, name):
        self.name = name
