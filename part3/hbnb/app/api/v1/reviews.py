from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services import facade

api = Namespace('reviews', description='Review operations')

# Define the review model for input validation and documentation
review_model = api.model('Review', {
    'text': fields.String(required=True, description='Text of the review'),
    'rating': fields.Integer(required=True, description='Rating of the place (1-5)'),
    'user_id': fields.String(required=True, description='ID of the user'),
    'place_id': fields.String(required=True, description='ID of the place')
})

@api.route('/')
class ReviewList(Resource):
    @jwt_required()
    @api.expect(review_model)
    @api.response(201, 'Review successfully created')
    @api.response(400, 'Invalid input data')
    @api.response(403, 'Unauthorized action')
    def post(self):
        """
        Register a new review (authenticated users only).
        Prevent reviewing own place and duplicate reviews.
        """
        current_user = get_jwt_identity()
        review_data = api.payload
        user_id = current_user["id"]
        place_id = review_data.get("place_id")

        # Prevent reviewing own place
        place = facade.get_place(place_id)
        if not place:
            return {"error": "Invalid place"}, 400
        if str(place.owner_id) == str(user_id):
            return {"error": "You cannot review your own place."}, 400

        # Prevent duplicate review for same place by same user
        all_reviews = facade.get_all_reviews()
        for review in all_reviews:
            if getattr(review, "user_id", None) == user_id and getattr(review, "place_id", None) == place_id:
                return {"error": "You have already reviewed this place."}, 400

        # Force user_id to be the current user
        review_data["user_id"] = user_id

        try:
            new_review = facade.create_review(review_data)
        except Exception as e:
            return {"error": str(e)}, 400

        return {
            "id": new_review.id,
            "text": new_review.text,
            "rating": new_review.rating,
            "user_id": new_review.user_id,
            "place_id": new_review.place_id
        }, 201

    @api.response(200, 'List of reviews retrieved successfully')
    def get(self):
        """
        Retrieve a list of all reviews.
        """
        review_repo_list = facade.get_all_reviews()
        reviews_list = []
        for review in review_repo_list:
            reviews_list.append({
                "id": review.id,
                "text": review.text,
                "rating": review.rating,
                "user_id": review.user_id,
                "place_id": review.place_id
            })
        return reviews_list, 200

@api.route('/<review_id>')
class ReviewResource(Resource):
    @api.response(200, 'Review details retrieved successfully')
    @api.response(404, 'Review not found')
    def get(self, review_id):
        """
        Get review details by ID.
        """
        review = facade.get_review(review_id)
        if not review:
            return {'error': 'Review not found'}, 404

        return {
            "id": review.id,
            "text": review.text,
            "rating": review.rating,
            "user_id": review.user_id,
            "place_id": review.place_id
        }, 200

    @jwt_required()
    @api.expect(review_model)
    @api.response(200, 'Review updated successfully')
    @api.response(404, 'Review not found')
    @api.response(400, 'Invalid input data')
    @api.response(403, 'Unauthorized action')
    def put(self, review_id):
        """
        Update a review's information (only creator).
        """
        current_user = get_jwt_identity()
        review_to_update = facade.get_review(review_id)
        if not review_to_update:
            return {'error': 'Review not found'}, 404
        if str(review_to_update.user_id) != str(current_user["id"]):
            return {"error": "Unauthorized action."}, 403

        update_review_data = api.payload
        try:
            facade.update_review(review_id, update_review_data)
        except Exception as e:
            return {"error": str(e)}, 400

        return {"message": "Review updated!"}, 200

    @jwt_required()
    @api.response(200, 'Review deleted successfully')
    @api.response(404, 'Review not found')
    @api.response(403, 'Unauthorized action')
    def delete(self, review_id):
        """
        Delete a review by ID (only creator).
        """
        current_user = get_jwt_identity()
        review = facade.get_review(review_id)
        if not review:
            return {'error': 'Review not found'}, 404
        if str(review.user_id) != str(current_user["id"]):
            return {"error": "Unauthorized action."}, 403

        facade.delete_review(review_id)
        return {"message": "Review deleted!"}, 200

@api.route('/places/<place_id>/reviews')
class PlaceReviewList(Resource):
    @api.response(200, 'List of reviews for the place retrieved successfully')
    @api.response(404, 'Place not found')
    def get(self, place_id):
        """
        Get all reviews for a specific place.
        """
        try:
            place_reviews = facade.get_reviews_by_place(place_id)
        except Exception as e:
            return {"error": str(e)}, 404

        reviews_list = []
        for review in place_reviews:
            reviews_list.append({
                "id": review.id,
                "text": review.text,
                "rating": review.rating,
                "user_id": review.user_id,
                "place_id": review.place_id
            })
        return reviews_list, 200
