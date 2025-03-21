from flask import request
from flask_restx import Namespace, Resource, fields ,abort
from ..model.car import Car, db
from datetime import datetime ,date
from ..model.Reservation import Reservation
import logging
from flask import session
logger = logging.getLogger(__name__)

car_ns = Namespace('car', description='Car related operations')

car_model = car_ns.model('Car', {
    'id': fields.Integer(readOnly=True, description='The id of the car'),
    'make': fields.String(required=True, description='The make of the car'),
    'model': fields.String(required=True, description='The model of the car'),
    'year': fields.Integer(required=True, description='The year of the car'),
    'price': fields.Float(required=True, description='The price of the car'),
    'status': fields.String(required=True, description='Rental status of the car'),
    'location': fields.String(required=True, description='The location of the car'),
    'type': fields.String(required=True, description='The type of the car'),
    'gearbox': fields.String(required=True, description='The gearbox of the')
})

@car_ns.route('/')
class ListCars(Resource):
    @car_ns.doc('list_cars')
    @car_ns.marshal_with(car_model, as_list=True)
    def get(self):
        location = request.args.get('location')
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        price = request.args.get('price')
        type = request.args.get('type')
        gearbox = request.args.get('gearbox')

        query = Car.query.filter(Car.status != 'NO')
        if location:
            query = query.filter(Car.location == location)

        if start_date and end_date:
            start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
            end_date = datetime.strptime(end_date, '%Y-%m-%d').date()
            query = query.filter(~Car.reservations.any(
                (Reservation.start_date <= end_date) & (Reservation.end_date >= start_date)
            ))

        if price:
            query = query.filter(Car.price <= float(price))

        if type:
            query = query.filter(Car.type == type)

        if gearbox:
            query = query.filter(Car.gearbox == gearbox)

        cars = query.all()
        return cars
    @car_ns.doc('add_car')
    @car_ns.expect(car_model, validate=True)
    @car_ns.marshal_with(car_model, code=201)
    def post(self):
        """Add a new car."""
        data = car_ns.payload
        existing_car = Car.query.filter_by(id=data['id']).first()
        if existing_car:
            abort(400, "Car with this ID already exists")
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
        car = Car.query.get_or_404(id)
        return car

    @car_ns.doc('update_car_status')
    @car_ns.expect(car_ns.model('CarStatusUpdate', {
        'status': fields.String(required=True, description='New rental status of the car')
    }), validate=True)
    @car_ns.response(200, 'Status updated successfully')
    def put(self, id):
        """Update the status of a car."""
        car = Car.query.get_or_404(id)
        data = request.get_json()
        new_status = data.get('status')
        if not new_status:
            abort(400, 'Status is required to update.')

        car.status = new_status
        db.session.commit()
        return {"message": "Car status updated successfully"}, 200


@car_ns.route('/reserve/<int:id>', methods=['POST'])
class ReserveCar(Resource):
    @car_ns.doc('reserve_car')
    @car_ns.expect(car_ns.model('Reservation', {
        'start_date': fields.Date(required=True),
        'end_date': fields.Date(required=True)
    }))
    def post(self, id):
        try:
            data = request.get_json()
            start_date = datetime.strptime(data['start_date'], '%Y-%m-%d').date()
            end_date = datetime.strptime(data['end_date'], '%Y-%m-%d').date()
            username = session.get('username')

            if not username:
                return {"message": "User not authenticated"}, 401

            if start_date < date.today():
                return {"message": "Start date cannot be in the past"}, 400

            if start_date >= end_date:
                return {"message": "Start date must be before end date"}, 400

            if Car.query.filter(Car.id == id).join(Reservation).filter(
                (Reservation.start_date <= end_date) &
                (Reservation.end_date >= start_date)).count() == 0:
                reservation = Reservation(car_id=id, start_date=start_date, end_date=end_date, username=username)
                db.session.add(reservation)
                db.session.commit()
                return {"message": "Reservation successful"}, 201
            else:
                return {"message": "Car not available for the selected dates"}, 400
        except Exception as e:
            logger.exception("Error while making reservation")
            db.session.rollback()
            return {"message": "An error occurred while making the reservation"}, 500