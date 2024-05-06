from ..app import db

class Sign_UP(db.Model):
    __tablename__ = 'sign_up'
    username = db.Column(db.String(20),primary_key=True,nullable=False)
    password = db.Column(db.String(100),nullable=False)
    reservations = db.relationship('Reservation', backref='renter', lazy=True)