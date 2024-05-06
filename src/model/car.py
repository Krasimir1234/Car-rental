from ..app import db

class Car(db.Model):
    __tablename__ = 'cars'

    id = db.Column(db.Integer, primary_key=True)
    make = db.Column(db.String(30), nullable=False)
    model = db.Column(db.String(30), nullable=False)
    year = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(30), nullable=False)
    location = db.Column(db.String(30), nullable=False)
    type = db.Column(db.String(50), nullable=True)
    gearbox = db.Column(db.String(30), nullable=True)
    owner_username = db.Column(db.String(20), db.ForeignKey('sign_up.username'))
    owner = db.relationship('Reservation', backref='carr', lazy=True, overlaps="carr,owner")

    def __init__(self,id: int, make: str, model: str, year: int, price: float,status:str ,location: str, type : str, gearbox: str):
        self.id = id
        self.make = make
        self.model = model
        self.year = year
        self.price = price
        self.status = status
        self.location = location
        self.type = type
        self.gearbox = gearbox
    def to_dict(self):# Takes the database data and makes it into a json
        return {
            'id': self.id,
            'make': self.make,
            'model': self.model,
            'year': self.year,
            'price': self.price,
            'status': self.status,
            'location': self.location,
            'type': self.type,
            'gearbox': self.gearbox
        }
    def add_to_database(self):#We add the data to the databse
        db.session.add(self)
        db.session.commit()

    @staticmethod
    def get_all_cars():# We get all the cars in the database
        return Car.query.all()
