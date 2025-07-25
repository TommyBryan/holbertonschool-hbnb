"""
users.py

This module defines the API endpoints for user operations, including user registration and retrieval.
It uses Flask-RESTX for API documentation and input validation.

Endpoints:
    POST /api/v1/users/      Register a new user (requires first_name, last_name, email, password)
    GET /api/v1/users/<id>   Retrieve user details by user ID

Notes:
    - Passwords are hashed before being stored.
    - Passwords are never returned in API responses.
    - Email addresses must be unique.
"""

from flask_restx import Namespace, Resource, fields
from app.services import facade
from werkzeug.security import generate_password_hash

def hash_password(password):
    """Hashes a password using Werkzeug's generate_password_hash."""
    return generate_password_hash(password)

# Create a Flask-RESTX namespace for user operations
api = Namespace('users', description='User operations')

# Define the user model for input validation and documentation
user_model = api.model('User', {
    'first_name': fields.String(required=True, description='First name of the user'),
    'last_name': fields.String(required=True, description='Last name of the user'),
    'email': fields.String(required=True, description='Email of the user'),
    'password': fields.String(required=True, description='Password of the user')
})

@api.route('/')
class UserList(Resource):
    @api.expect(user_model, validate=True)
    @api.response(201, 'User successfully created')
    @api.response(400, 'Email already registered')
    @api.response(400, 'Invalid input data')
    def post(self):
        """
        Register a new user

        This endpoint allows the creation of a new user. It expects a JSON payload
        containing the user's first name, last name, email, and password. The email
        must be unique, and the password will be hashed before storage.
        """
        user_data = api.payload  # Get JSON payload from request

        # Check if the email is already registered
        existing_user = facade.get_user_by_email(user_data['email'])
        if existing_user:
            return {'error': 'Email already registered'}, 400

        try:
            # Hash the password before storing in the database
            user_data['password'] = hash_password(user_data['password'])
            # Create the user using the facade service
            new_user = facade.create_user(user_data)
        except Exception as e:
            # Handle invalid input or creation errors
            return {"error": f"Invalid input data {e}"}, 400

        # Return only the user ID and a success message (never return password)
        return {
            'id': new_user.id,
            'message': "User successfully created"
            }, 201
    
    
@api.route('/<user_id>')
class UserResource(Resource):
    @api.response(200, 'User details retrieved successfully')
    @api.response(404, 'User not found')
    def get(self, user_id):
        """Get user details by ID

        Retrieves the user's id, first name, last name, and email.
        The password is never returned.
        """
        user = facade.get_user(user_id)  # Retrieve user by ID
        if not user:
            return {'error': 'User not found'}, 404
        # Return user details, excluding the password
        return {
            'id': user.id,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email
        }, 200
