from app.persistence.repository import SQLAlchemyRepository
from app.models.user import User
from app.models.place import Place
from app.models.amenity import Amenity
from app.models.review import Review

class HBnBFacade:
    def __init__(self):
        self.user_repo = SQLAlchemyRepository(User)

    """ User facade. """
    def create_user(self, user_data):
        user = User(**user_data)
        self.user_repo.add(user)
        return user

    def get_user(self, user_id):
        return self.user_repo.get(user_id)

    def get_user_by_email(self, email):
        return self.user_repo.get_by_attribute('email', email)

    def update_user(self, user_id, user_data):
        self.user_repo.update(user_id, user_data)

    """ Amenity facade. """

    def create_amenity(self, amenity_data):
        amenity = Amenity(**amenity_data)
        self.amenity_repo.add(amenity)
        return amenity

    def get_amenity(self, amenity_id):
        return self.amenity_repo.get(amenity_id)

    def get_all_amenities(self):
        """
        Retrieve all amenities.
        """
        return self.amenity_repo.get_all()

    def update_amenity(self, amenity_id, amenity_data):
        self.amenity_repo.update(amenity_id, amenity_data)

    """ PLaces facade. """

    def create_place(self, place_data):
        """
        Create a place and add it to the repository.
        """
        place = Place(**place_data)
        self.place_repo.add(place)
        return place

    def get_place(self, place_id):
        """
        Retrieve a place by its ID.
        """
        return self.place_repo.get(place_id)

    def get_all_places(self):
        """
        Retrieve all places.
        """
        return self.place_repo.get_all()

    def update_place(self, place_id, place_data):
        """
        Update a place's information.
        """
        self.place_repo.update(place_id, place_data)

    """ Review facade. """

    def create_review(self, review_data):
        """
        Create a review.
        """
        review = Review(**review_data)
        self.review_repo.add(review)
        return review

    def get_review(self, review_id):
        """
        Get a single review.
        """
        return self.review_repo.get(review_id)

    def get_all_reviews(self):
        """
        Get all reviews.
        """
        return self.review_repo.get_all()

    def get_reviews_by_place(self, place_id):
        """
        Get review by place.
        """
        place = self.place_repo.get(place_id)
        if not place:
            return []
        reviews = [self.review_repo.get(review_id) for review_id in getattr(place, "reviews", [])]
        return [r for r in reviews if r]

    def update_review(self, review_id, review_data):
        """
        Update review.
        """
        self.review_repo.update(review_id, review_data)

    def delete_review(self, review_id):
        """
        Delete review.
        """
        self.review_repo.delete(review_id)
