from app.models.base_class import BaseModel


class Place(BaseModel):
    def __init__(self, title, price, latitude, longitude, owner, description=""):
        super().__init__()
        self.title = title
        self.description = description
        self.price = price
        self.latitude = latitude
        self.longitude = longitude
        self._owner = owner
        self._reviews = []  # List to store related reviews
        self._amenities = []  # List to store related amenities

    def add_review(self, review):
        """ Add a review to the place."""
        from .review import Review
        if not isinstance(review, Review):
            raise TypeError("Review must be an instance of Review")
        self._reviews.append(review)

    def remove_review(self, review):
        """ Remove a review from the place."""
        if review in self._reviews:
            self._reviews.remove(review)
        
    @property
    def reviews(self):
        """
        Get the list of reviews of the place.
        
        Returns:
            list: List of Reviews.
        """
        return self._reviews
    
    @reviews.setter
    def reviews(self, reviews):
        if not isinstance(reviews, list):
            raise TypeError("Reviews must be a list")
        self._reviews = []


    @property
    def title(self):
        return self._title
    
    @title.setter
    def title(self, title):
        if not isinstance(title, str):
            raise TypeError("Title must be a string")
        if len(title) > 100:
            raise ValueError("Maximum length is 100 characters")
        self._title = title
    
    @property
    def description(self):
        return self._description
    
    @description.setter
    def description(self, description):
        if not isinstance(description, str):
            raise TypeError("Description must be a string")
        if len(description) > 500:
            raise ValueError("Maximum length is 500 characters")
        self._description = description

    @property
    def price(self):
        return self._price
    
    @price.setter
    def price(self, price):
        if not isinstance(price, (int, float)):
            raise TypeError("Price must be a float")
        if price < 0:
            raise ValueError("Price must be a positive number")
        self._price = price

    @property
    def longitude(self):
        return self._longitude
    
    @longitude.setter
    def longitude(self, longitude):
        if not isinstance(longitude, float):
            raise TypeError("Longitude must be a float")
        if longitude < -180.0 or longitude > 180.0:
            raise ValueError("Longitude must be between the range -180 and 180")
        self._longitude = longitude

    @property
    def latitude(self):
        return self._latitude
    
    @latitude.setter
    def latitude(self, latitude):
        if not isinstance(latitude, float):
            raise TypeError("Latitude must be a float")
        if latitude < -90 or latitude > 90:
            raise ValueError("Latitude must be between the range -90 and 90")
        self._latitude = latitude

    @property
    def owner(self):
        return self._owner

    @owner.setter
    def owner(self, owner):
        from .user import User
        if not isinstance(owner, User):
            raise TypeError("Owner must be a User instance")
        self._owner = owner
