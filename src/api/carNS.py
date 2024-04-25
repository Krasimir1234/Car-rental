from flask import jsonify ,request
from flask_restx import Namespace, Resource, fields
from random import randint
from ..database import db
from src.model.car import Car

car_ns = Namespace('car', description='car related operations')

car_model = car_ns.model('Car model',{
    'id' : fields.Integer(required=True,
                          help= 'The id of the car'),
    'make': fields.String(required=True,
                          help= 'The make of the car'),
    'model': fields.String(required=True,
                           help= 'The model of the car'),
    'year': fields.Integer(required=True,
                           help= 'The year of the car'),
    'price': fields.Float(required=True,
                          help= 'The price of the car')
})



@car_ns.route('/')
class ListCars(Resource):
    @car_ns.doc(car_model, description='Add a car to the list of cars')
    @car_ns.expect(car_model,validate=True)
    @car_ns.marshal_with(car_model)
    def post(self):
        car_id = randint(1,10000)

        new_car = Car(id=car_id,
                      make=car_ns.payload['make'],
                      model=car_ns.payload['model'],
                      year=car_ns.payload['year'],
                      price=car_ns.payload['price'])

        db.session.add(new_car)
        db.session.commit()
        return new_car

    @car_ns.marshal_with(car_model)
    def get(self):
        return Car.query.all()
