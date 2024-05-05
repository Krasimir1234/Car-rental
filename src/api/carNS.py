from flask import request
from flask_restx import Namespace, Resource, fields
from ..model.car import Car, db

car_ns = Namespace('car', description='Car related operations')

car_model = car_ns.model('Car', {
    'id': fields.Integer(readOnly=True, description='The id of the car'),
    'make': fields.String(required=True, description='The make of the car'),
    'model': fields.String(required=True, description='The model of the car'),
    'year': fields.Integer(required=True, description='The year of the car'),
    'price': fields.Float(required=True, description='The price of the car'),
    'status': fields.String(required=True, description='Rental status of the car'),
    'location': fields.String(required=True, description='The location of the car')
})

@car_ns.route('/')
class ListCars(Resource):
    @car_ns.doc('list_cars')
    @car_ns.marshal_with(car_model, as_list=True)
    def get(self):
        """List all cars or filter cars by location."""
        location = request.args.get('location')
        if location:
            cars = Car.query.filter(Car.location == location, Car.status != 'NO').all()
        else:
            cars = Car.query.filter(Car.status != 'NO').all()
        return cars

    @car_ns.doc('add_car')
    @car_ns.expect(car_model, validate=True)
    @car_ns.marshal_with(car_model, code=201)
    def post(self):
        """Add a new car."""
        data = car_ns.payload
        new_car = Car(**data)
        new_car.add_to_database()
        return new_car, 201

@car_ns.route('/<int:id>')
@car_ns.response(404, 'Car not found')
@car_ns.param('id', 'The car identifier')
class CarResource(Resource):
    @car_ns.doc('get_car')
    @car_ns.marshal_with(car_model)
    def get(self, id):
        """Fetch a car given its identifier."""
        car = Car.query.get_or_404(id)# if it doesnt exist it trows a 404
        return car
