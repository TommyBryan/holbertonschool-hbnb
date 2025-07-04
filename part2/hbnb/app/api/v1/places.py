from flask_restx import Namespace, Resource, fields
from app.services import facade

api = Namespace('places', description='Place operations')

# Define the models for related entities
amenity_model = api.model('PlaceAmenity', {
    'id': fields.String(description='Amenity ID'),
    'name': fields.String(description='Name of the amenity')
})

user_model = api.model('PlaceUser', {
    'id': fields.String(description='User ID'),
    'first_name': fields.String(description='First name of the owner'),
    'last_name': fields.String(description='Last name of the owner'),
    'email': fields.String(description='Email of the owner')
})

# Define the place model for input validation and documentation
place_model = api.model('Place', {
    'title': fields.String(required=True, description='Title of the place'),
    'description': fields.String(description='Description of the place'),
    'price': fields.Float(required=True, description='Price per night'),
    'latitude': fields.Float(required=True, description='Latitude of the place'),
    'longitude': fields.Float(required=True, description='Longitude of the place'),
    'owner_id': fields.String(required=True, description='ID of the owner'),
    'amenities': fields.List(fields.String, required=True, description="List of amenities ID's")
})

@api.route('/')
class PlaceList(Resource):
    @api.expect(place_model)
    @api.response(201, 'Place successfully created')
    @api.response(400, 'Invalid input data')
    def post(self):
        """Register a new place"""
        place_data = api.payload
        if not facade.get_user(place_data["owner_id"]):
            return {"error": "Invalid input data"}, 400

        try:
            new_place = facade.create_place(place_data)
        except Exception:
            return {"error": "Invalid input data"}, 400
        facade.update_user(new_place.owner_id, {"places": new_place.id})

        return {
            "id": new_place.id,
            "title": new_place.title,
            "description": new_place.description,
            "price": new_place.price,
            "latitude": new_place.latitude,
            "longitude": new_place.longitude,
            "owner_id": new_place.owner_id
        }, 201

    @api.response(200, 'List of places retrieved successfully')
    def get(self):
        """Retrieve a list of all places"""
        place_repo_list = facade.get_all_places()
        places_list = []
        for place in place_repo_list:
            places_list.append(
                {
                    "id": place.id,
                    "title": place.title,
                    "latitude": place.latitude,
                    "longitude": place.longitude
                }
            )
        return places_list, 200

@api.route('/<place_id>')
class PlaceResource(Resource):
    @api.response(200, 'Place details retrieved successfully')
    @api.response(404, 'Place not found')
    def get(self, place_id):
        """Get place details by ID"""
        place = facade.get_place(place_id)
        if not place:
            return {"error": "Place not found"}, 404

        owner = facade.get_user(place.owner_id)
        amenities = [facade.get_amenity(amenity) for amenity in place.amenities]
        reviews = [facade.get_review(review) for review in place.reviews]

        # Manually build the response dictionaries
        owner_dict = {
            "id": owner.id,
            "first_name": owner.first_name,
            "last_name": owner.last_name,
            "email": owner.email
        } if owner else None

        amenities_list = [
            {"id": amenity.id, "name": amenity.name}
            for amenity in amenities if amenity
        ]

        reviews_list = [
            {
                "id": review.id,
                "user_id": review.user_id,
                "text": review.text,
                "rating": review.rating
            }
            for review in reviews if review
        ]

        return {
            "id": place.id,
            "title": place.title,
            "description": place.description,
            "latitude": place.latitude,
            "longitude": place.longitude,
            "owner": owner_dict,
            "amenities": amenities_list,
            "reviews": reviews_list
        }, 200

    @api.expect(place_model)
    @api.response(200, 'Place updated successfully')
    @api.response(404, 'Place not found')
    @api.response(400, 'Invalid input data')
    def put(self, place_id):
        """Update a place's information"""
        place = facade.get_place(place_id)
        if not place:
            return {"error": "Place not found"}, 404

        update_data = api.payload
        try:
            facade.update_place(place_id, update_data)
        except Exception:
            return {"error": "Invalid input data"}, 400

        updated_place = facade.get_place(place_id)
        return {
            "id": updated_place.id,
            "title": updated_place.title,
            "description": updated_place.description,
            "price": updated_place.price,
            "latitude": updated_place.latitude,
            "longitude": updated_place.longitude,
            "owner_id": updated_place.owner_id
        }, 200
