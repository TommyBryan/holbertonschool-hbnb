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

    def __init__(self, text, rating, place, user):
        """Initialize a review instance"""
        super().__init__()
        self.text = self._validate_text(text)
        self.rating = self._validate_rating(rating)
        self.place = self._validate_place(place)
        self.user_id = self._validate_user(user)

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

    def _validate_place(self, place):
        """Validates that place is a valid Place instance"""
        if not isinstance(place, Place):
            raise ValueError("Place must be a valid Place instance")
        return place.id

    def _validate_user(self, user):
        """Validates that user is a valid User instance"""
        if not isinstance(user, User):
            raise ValueError("User must be a valid User instance")
        return user.id
