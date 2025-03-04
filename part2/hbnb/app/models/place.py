from app.models.base_model import BaseModel
from app.models.user import User
from app.models.amenity import Amenity
from app.models.review import Review

class Place(BaseModel):
    def __init__(self, title, description, price, latitude, longitude, owner):
        super().__init__()
        self.title = title
        self.description = description
        self.price = price
        self.latitude = latitude
        self.longitude = longitude
        self.owner = owner
        self.reviews = []  # List to store related reviews
        self.amenities = []  # List to store related amenities

        self.validate_title()
        self.validate_price()
        self.validate_latitude()
        self.validate_longitude()

    def validate_title(self):
        if len(self.title) > 100:
            raise ValueError("Title cannot exceed 100 characters")

    def validate_price(self):
        if self.price <= 0:
            raise ValueError("Price must be a positive value")

    def validate_latitude(self):
        if not (-90.0 <= self.latitude <= 90.0):
            raise ValueError("Latitude must be between -90.0 and 90.0")

    def validate_longitude(self):
        if not (-180.0 <= self.longitude <= 180.0):
            raise ValueError("Longitude must be between -180.0 and 180.0")

    def add_review(self, review):
        """Add a review to the place."""
        self.reviews.append(review)

    def add_amenity(self, amenity):
        """Add an amenity to the place."""
        self.amenities.append(amenity)
