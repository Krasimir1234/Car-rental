from flask import request, session
from flask_restx import Namespace, Resource, fields
from ..model.signup import Sign_UP
from ..app import db

auth_ns = Namespace('auth', description='Authentication related operations')

signup_model = auth_ns.model('Signup', {
    'username': fields.String(required=True, description='The username of the user'),
    'password': fields.String(required=True, description='The password of the user')
})
login_model = auth_ns.model('Login', {
    'username': fields.String(required=True, description='The username of the user'),
    'password': fields.String(required=True, description='The password of the user')
})

@auth_ns.route('/signup')
class SignUp(Resource):
    @auth_ns.doc('signup')
    @auth_ns.expect(signup_model, validate=True)
    def post(self):
        """Sign up a new user."""
        data = auth_ns.payload  # Extract JSON payload from the request
        # Create a new user object with the provided data
        new_user = Sign_UP(username=data['username'], password=data['password'])
        # Add the new user to the database session
        db.session.add(new_user)
        # Commit the transaction to persist the new user in the database
        db.session.commit()
        # Return a success message with status code 201
        return {"message": "User signed up successfully"}, 201



@auth_ns.route('/login')
class UserLogin(Resource):
    @auth_ns.doc('login')
    @auth_ns.expect(login_model, validate=True)
    def post(self):
        """Log in an existing user."""
        data = auth_ns.payload
        username = data['username']
        password = data['password']
        user = Sign_UP.query.filter_by(username=username, password=password).first()
        if user:
            # Log in successful
            session['username'] = username  # Set session variable

            # Check if session variable is set
            if 'username' in session:
                print("Session variable 'username' is set:", session['username'])

            return {"message": "Login successful"}, 200
        else:
            # Incorrect username or password
            return {"message": "Invalid username or password"}, 401

