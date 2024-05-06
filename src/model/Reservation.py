from ..app import db
class Reservation(db.Model):
    __tablename__ = 'reservation'
    id = db.Column(db.Integer, primary_key=True)
    car_id = db.Column(db.Integer, db.ForeignKey('cars.id'), nullable=False)
    username = db.Column(db.String(20), db.ForeignKey('sign_up.username'), nullable=False)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)
    car = db.relationship('Car', backref=db.backref('reservations', lazy=True))
    @staticmethod
    def create_reservation(start_date, end_date, car_id, username):
        new_reservation = Reservation(
            start_date=start_date,
            end_date=end_date,
            car_id=car_id,
            username=username
        )
        db.session.add(new_reservation)
        db.session.commit()

    @staticmethod
    def cancel_reservation(reservation_id):
        reservation = Reservation.query.get(reservation_id)
        if reservation:
            db.session.delete(reservation)
            db.session.commit()
        else:
            raise ValueError("Reservation not found")