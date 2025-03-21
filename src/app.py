from flask import Flask, render_template, request ,session ,redirect ,url_for ,flash
from flask_restx import Api
from .database import db
from .api.carNS import car_ns
from .model.car import Car
from .api.signupNS import auth_ns
from .model.secrets import Config
from .model.signup import Sign_UP
from .model.Reservation import Reservation
import logging
def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cars.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.secret_key = Config.SECRET_KEY
    db.init_app(app)

    with app.app_context():
            db.create_all()

    api = Api(app, title='An app for a car rental company')
    api.add_namespace(car_ns, path='/api/cars')
    api.add_namespace(auth_ns)

    @app.route('/admin')
    def admin():
        return render_template('admin.html')

    @app.route('/signup')
    def signup():
        return render_template('Signup.html')

    @app.route('/Login', methods=['GET', 'POST'])
    def login():
        if request.method == 'POST':
            username = request.form['username']
            password = request.form['password']


            if username == 'valid_username' and password == 'valid_password':
                session['username'] = username
                return redirect(url_for('home'))
            else:
                flash('Invalid username or password')
        return render_template('login.html')

    @app.route('/home')
    def home():
        if 'username' in session:
            location = request.args.get('location')
            cars = Car.query.filter(Car.location == location, Car.status != 'NO').all() if location else []
            return render_template('Home.html', cars=cars, location=location, username=session['username'])
        else:
            return redirect(url_for('login'))

    return app
