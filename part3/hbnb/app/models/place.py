#!/usr/bin/python3
"""Place Model"""
from app.extensions import db
from .base_class import BaseModel

place_amenity = db.Table(
    'place_amenity',
    db.Column('place_id', db.String(36), db.ForeignKey('places.id'), primary_key=True),
    db.Column('amenity_id', db.String(36), db.ForeignKey('amenities.id'), primary_key=True)
)

class Place(BaseModel):
    """Represents a rental property in the database."""
    __tablename__ = "places"

    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=True)
    price = db.Column(db.Float, nullable=False)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    # Temporarily store as String without foreign key constraint
    owner_id = db.Column(db.String(36), nullable=False)

    # Relationship
    owner = db.relationship('User', back_populates='places')
    reviews = db.relationship('Review', back_populates='place', cascade="all, delete-orphan")
    amenities = db.relationship('Amenity', secondary=place_amenity, back_populates='places')

    def __init__(self, title, description, price, latitude, longitude, owner_id):
        super().__init__()
        self.title = self._validate_string(title, "Title")
        self.description = self._validate_string(description, "Description")
        self.price = self._validate_price(price)
        self.latitude = self._validate_coordinate(latitude, "Latitude")
        self.longitude = self._validate_coordinate(longitude, "Longitude")
        self.owner_id = owner_id

    def _validate_string(self, value, field_name):
        """Validates that a value is a non-empty string"""
        if not isinstance(value, str) or not value.strip():
            raise ValueError(f"{field_name} must be a non-empty string")
        return value.strip()

    def _validate_price(self, value):
        """Validates that price is a positive float."""
        if not isinstance(value, (int, float)) or value < 0:
            raise ValueError("Price must be a positive number")
        return float(value)

    def _validate_coordinate(self, value, field_name):
        """Validates latitude/longitude as a valid float."""
        if not isinstance(value, (int, float)) or not (-180 <= value <= 180):
            raise ValueError(f"{field_name} must be a valid coordinate")
        return float(value)

    def _validate_owner(self, owner_id):
        """Validates that the owner exists"""
        from app.services import facade
        owner = facade.get_user(owner_id)
        if not owner:
            raise ValueError("Owner must be a valid User")
        return owner_id

    def add_review(self, review):
        """add a review to the place"""
        from .review import Review

        if not isinstance(review, Review):
            raise ValueError("Invalid review")
        self.reviews.append(review)

    def add_amenity(self, amenity):
        """add amenity to the place"""
        from .amenity import Amenity  # Avoid circular import

        if not isinstance(amenity, Amenity):
            raise ValueError("Invalid amenity")
        self.amenities.append(amenity)

    def __repr__(self):
        """Returns a string representation of the Place object"""
        return (f"Place(title='{self.title}', price={self.price}, "
                f"latitude={self.latitude}, longitude={self.longitude}, "
                f"owner='{self.owner}', reviews={len(self.reviews)}, "
                f"amenities={len(self.amenities)})")

    def to_dict(self):
        """Convert place to dictionary"""
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'price': self.price,
            'latitude': self.latitude,
            'longitude': self.longitude,
            'owner_id': self.owner_id,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }
