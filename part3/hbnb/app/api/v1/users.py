from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services import facade

api = Namespace('users', description='User operations')

# Define the user model for input validation and documentation
user_model = api.model('User', {
    'first_name': fields.String(required=True, description='First name of the user'),
    'last_name': fields.String(required=True, description='Last name of the user'),
    'email': fields.String(required=True, description='Email of the user'),
    'password': fields.String(required=True, description='Password for the user')
})

@api.route('/')
class UserList(Resource):
    @api.expect(user_model, validate=True)
    @api.response(201, 'User successfully created')
    @api.response(400, 'Email already registered')
    @api.response(400, 'Invalid input data')
    def post(self):
        """Register a new user"""
        user_data = api.payload

        # Simulate email uniqueness check (to be replaced by real validation with persistence)
        existing_user = facade.get_user_by_email(user_data['email'])
        if existing_user:
            return {'error': 'Email already registered'}, 400

        try:
            new_user = facade.create_user(user_data)
        except Exception as e:
            return {"error": f"Invalid input data {e}"}, 400

        return {
            'id': new_user.id,
            'message': "User successfully created"
            }, 201
    
@api.route('/<user_id>')
class UserResource(Resource):
    @api.response(200, 'User details retrieved successfully')
    @api.response(404, 'User not found')
    def get(self, user_id):
        """Get user details by ID"""
        user = facade.get_user(user_id)
        if not user:
            return {'error': 'User not found'}, 404
        
        return {
            'id': user.id,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email,
            'places': user.places,
        }, 200

    @jwt_required()
    @api.response(200, 'User updated successfully')
    @api.response(404, 'User not found')
    @api.response(403, 'Unauthorized action')
    @api.response(400, 'Invalid input data')
    def put(self, user_id):
        """Update user info (only self, cannot change email or password)"""
        current_user = get_jwt_identity()
        if str(current_user["id"]) != str(user_id):
            return {"error": "Unauthorized action."}, 403

        user = facade.get_user(user_id)
        if not user:
            return {'error': 'User not found'}, 404

        update_data = api.payload or {}
        # Prevent changing email or password
        if "email" in update_data or "password" in update_data:
            return {"error": "You cannot modify email or password."}, 400
        try:
            facade.update_user(user_id, update_data)
        except Exception as e:
            return {"error": f"Invalid input data {e}"}, 400

        updated_user = facade.get_user(user_id)
        return {
            'id': updated_user.id,
            'first_name': updated_user.first_name,
            'last_name': updated_user.last_name,
            'email': updated_user.email,
            'places': updated_user.places,
        }, 200
