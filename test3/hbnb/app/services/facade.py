from app.persistence.repository import SQLAlchemyRepository
from app.models.user import User
from app.persistence.user_repository import UserRepository
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
class HBnBFacade:
    def __init__(self):
        self.user_repo = UserRepository()

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

    def create_amenity(self, amenity_data):
        pass

    def get_amenity(self, amenity_id):
        pass

    def get_all_amenities(self):
        pass

    def update_amenity(self, amenity_id, amenity_data):
        pass

    def create_place(self, place_data):
        pass

    def get_place(self, place_id):
        pass

    def get_all_places(self):
        pass

    def update_place(self, place_id, place_data):
        pass

    def create_review(self, review_data):
        pass

    def get_review(self, review_id):
        pass

    def get_all_reviews(self):
        pass

    def get_reviews_by_place(self, place_id):
        pass

    def update_review(self, review_id, review_data):
        pass

    def delete_review(self, review_id):
        pass
