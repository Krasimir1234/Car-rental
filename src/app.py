from flask import Flask,render_template
from flask_restx import Api
from .database import db
from .api.carNS import car_ns

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
    api.add_namespace(car_ns)
    @app.route('/admin')
    def index():
        return render_template('home.html')
    return app