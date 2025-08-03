from app.persistence.repository import SQLAlchemyRepository
from app.models.user import User
from app.models.place import Place
from app.models.review import Review
from app.models.amenity import Amenity
from app.persistence.user_repository import UserRepository
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class HBnBFacade:
    def __init__(self):
        self.user_repo = UserRepository()
        self.place_repo = SQLAlchemyRepository(Place)
        self.review_repo = SQLAlchemyRepository(Review) 
        self.amenity_repo = SQLAlchemyRepository(Amenity)

    def create_user(self, user_data):
        """Store a User instance"""
        user = User(**user_data)
        # Password is already hashed in User.__init__, no need to hash again
        self.user_repo.add(user)
        return user

    def get_user(self, user_id):
        return self.user_repo.get(user_id)

    def get_user_by_email(self, email):
        return self.user_repo.get_by_attribute('email', email)

    def get_all_reviews(self):
        """Get all reviews"""
        return self.review_repo.get_all()

    def create_amenity(self, amenity_data):
        """Create a new amenity"""
        from app.models.amenity import Amenity
        amenity = Amenity(**amenity_data)
        self.amenity_repo.add(amenity)
        return amenity

    def get_amenity(self, amenity_id):
        """Get amenity by ID"""
        return self.amenity_repo.get(amenity_id)

    def get_all_amenities(self):
        """Get all amenities"""
        return self.amenity_repo.get_all()

    def update_amenity(self, amenity_id, amenity_data):
        """Update amenity"""
        return self.amenity_repo.update(amenity_id, amenity_data)

    def create_place(self, place_data):
        """Create a new place"""
        place = Place(**place_data)
        self.place_repo.add(place)
        return place

    def get_place(self, place_id):
        """Get place by ID"""
        return self.place_repo.get(place_id)

    def get_all_places(self):
        """Get all places"""
        return self.place_repo.get_all()

    def update_place(self, place_id, place_data):
        """Update place"""
        return self.place_repo.update(place_id, place_data)

    def create_review(self, review_data):
        """Create a new review"""
        review = Review(**review_data)
        self.review_repo.add(review)
        return review

    def get_review(self, review_id):
        """Get review by ID"""
        return self.review_repo.get(review_id)

    def get_review_by_user_and_place(self, user_id, place_id):
        """Check if user already reviewed a place"""
        # Get all reviews and filter by user_id and place_id
        reviews = self.review_repo.get_all()
        for review in reviews:
            if review.user_id == user_id and review.place_id == place_id:
                return review
        return None

    def get_reviews_by_place(self, place_id):
        """Get all reviews for a specific place"""
        all_reviews = self.review_repo.get_all()
        return [review for review in all_reviews if review.place_id == place_id]

    def update_review(self, review_id, review_data):
        """Update review"""
        return self.review_repo.update(review_id, review_data)

    def delete_review(self, review_id):
        """Delete a review"""
        review = self.review_repo.get(review_id)
        if not review:
            raise ValueError("Review not found")
        return self.review_repo.delete(review_id)

    def update_user(self, user_id, user_data):
        """Update user"""
        return self.user_repo.update(user_id, user_data)
