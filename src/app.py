from flask import Flask,render_template,request
from flask_restx import Api
from .database import db
from .api.carNS import car_ns
from .model.car import Car
def create_app():
    app = Flask(__name__)
    # Connecting and making the database with flask-sqlalchemy
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cars.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    # Initialize the db
    db.init_app(app)
    with app.app_context():
        db.create_all()
    api = Api(app, title='An app for a car rental company')
    api.add_namespace(car_ns, path='/api/cars')
    @app.route('/admin')
    def index():
        return render_template('admin.html')

    @app.route('/home')
    def index2():
        location = request.args.get('location')
        cars = Car.query.filter(Car.location == location, Car.status != 'NO').all() if location else []
        return render_template('Home.html', cars=cars, location=location)
    return app