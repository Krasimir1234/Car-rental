from ..app import db

class Car(db.Model):
    __tablename__ = 'cars'

    id = db.Column(db.Integer, primary_key=True)
    make = db.Column(db.String(30), nullable=False)
    model = db.Column(db.String(30), nullable=False)
    year = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Float, nullable=False)



    def __init__(self,id: int, make: str, model: str, year: int, price: float):
        self.id = id
        self.make = make
        self.model = model
        self.year = year
        self.price = price

    def to_dict(self):
        return {
            'id': self.id,
            'make': self.make,
            'model': self.model,
            'year': self.year,
            'price': self.price
        }
    def add_to_database(self):
        db.session.add(self)
        db.session.commit()

    @staticmethod
    def get_all_cars():
        return Car.query.all()
