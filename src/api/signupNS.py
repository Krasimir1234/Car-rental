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
        data = auth_ns.payload
        new_user = Sign_UP(username=data['username'], password=data['password'])
        db.session.add(new_user)
        db.session.commit()
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
            session['username'] = username

            if 'username' in session:
                print("Session variable 'username' is set:", session['username'])

            return {"message": "Login successful"}, 200
        else:
            return {"message": "Invalid username or password"}, 401

