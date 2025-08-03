#!/usr/bin/python3
from app import db
from .base_class import BaseModel


class Review(BaseModel):
    """Represents a user review for a place."""
    __tablename__ = 'reviews'

    text = db.Column(db.Text, nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    place_id = db.Column(db.Integer, db.ForeignKey('places.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    # Relationship
    place = db.relationship('Place', back_populates='reviews')
    user = db.relationship('User', back_populates='reviews')

    __table_args__ = (
        db.CheckConstraint('rating >= 1 AND rating <= 5', name='rating_range'),
    )

    def __init__(self, text, rating, place_id, user_id):
        """Initialize a review instance"""
        super().__init__()
        self.text = self._validate_text(text)
        self.rating = self._validate_rating(rating)
        self.place_id = place_id
        self.user_id = user_id

    def _validate_text(self, text):
        """Validates that text is a non-empty string"""
        if not isinstance(text, str) or not text.strip():
            raise ValueError("Review text must be a non-empty string")
        return text.strip()

    def _validate_rating(self, rating):
        """Validates that rating is between 1 and 5"""
        if not isinstance(rating, int) or not (1 <= rating <= 5):
            raise ValueError("Rating must be an integer between 1 and 5")
        return rating

    def _validate_place(self, place_id):
        """Validates that place_id exists"""
        # Remove Place instance validation, just validate ID exists
        from app.services import facade
        place = facade.get_place(place_id)
        if not place:
            raise ValueError("Place does not exist")
        return place_id

    def _validate_user(self, user_id):
        """Validates that user_id exists"""
        # Remove User instance validation, just validate ID exists
        from app.services import facade
        user = facade.get_user(user_id)
        if not user:
            raise ValueError("User does not exist")
        return user_id

    def to_dict(self):
        """Convert review to dictionary"""
        return {
            'id': self.id,
            'text': self.text,
            'rating': self.rating,
            'place_id': self.place_id,
            'user_id': self.user_id,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }
