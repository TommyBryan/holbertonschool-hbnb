from app.models.user import User
from app.models.place import Place
from app.models.review import Review
from app.models.amenity import Amenity
from app.persistence.repository import SQLAlchemyRepository

class HBnBFacade:
    def __init__(self):
        self.user_repo = SQLAlchemyRepository(User)
        self.place_repo = SQLAlchemyRepository(Place)
        self.review_repo = SQLAlchemyRepository(Review)
        self.amenity_repo = SQLAlchemyRepository(Amenity)

    def create_user(self, user_data):
        """Store a User instance"""
        user = User(**user_data)
        # Hash the password before saving
        if 'password' in user_data:
            user.hash_password(user_data['password'])
        self.user_repo.add(user)
        return user

    def get_user(self, user_id):
        """Retrieve a user by ID"""
        return self.user_repo.get(user_id)

    def get_user_by_email(self, email):
        """Retrieve a user by email"""
        return self.user_repo.get_by_attribute('email', email)

    def update_user(self, user_id, user_data):
        """Update a user"""
        return self.user_repo.update(user_id, user_data)

    def create_place(self, place_data):
        """Create a new place"""
        place = Place(**place_data)
        self.place_repo.add(place)
        return place

    def get_place(self, place_id):
        """Retrieve a place by ID"""
        return self.place_repo.get(place_id)

    def get_all_places(self):
        """Retrieve all places"""
        return self.place_repo.get_all()

    def update_place(self, place_id, place_data):
        """Update a place"""
        return self.place_repo.update(place_id, place_data)

    def create_review(self, review_data):
        """Create a new review"""
        review = Review(**review_data)
        self.review_repo.add(review)
        return review

    def get_review(self, review_id):
        """Retrieve a review by ID"""
        return self.review_repo.get(review_id)

    def get_all_reviews(self):
        """Retrieve all reviews"""
        return self.review_repo.get_all()

    def get_reviews_by_place(self, place_id):
        """Get all reviews for a specific place"""
        all_reviews = self.review_repo.get_all()
        return [review for review in all_reviews if review.place_id == place_id]

    def update_review(self, review_id, review_data):
        """Update a review"""
        return self.review_repo.update(review_id, review_data)

    def delete_review(self, review_id):
        """Delete a review"""
        return self.review_repo.delete(review_id)

    def create_amenity(self, amenity_data):
        """Create a new amenity"""
        amenity = Amenity(**amenity_data)
        self.amenity_repo.add(amenity)
        return amenity

    def get_amenity(self, amenity_id):
        """Retrieve an amenity by ID"""
        return self.amenity_repo.get(amenity_id)

    def get_all_amenities(self):
        """Retrieve all amenities"""
        return self.amenity_repo.get_all()

    def update_amenity(self, amenity_id, amenity_data):
        """Update an amenity"""
        return self.amenity_repo.update(amenity_id, amenity_data)
