from base_class import BaseModel

class Place(BaseModel):
    def __init__(self, title: str, description: str, price: float, latitude: float, longitude: float,  owner):
        self.title = title
        self.description = description
        self.price = price
        self.latitude = latitude
        self.longitude = longitude
        self.owner = owner

    def validate_title(self, title):
        if not isinstance(title, str):
            raise TypeError("Title must be a string")
        if len(title) > 100:
            raise ValueError("Maximum length is 100 characters")
        
    def validate_price(self, price):
        if not isinstance(price, float):
            raise TypeError("Price must be a float")
        if price < 0:
            raise ValueError("Price must be a positive number")
        
    def validate_longitud(self, longitude):
        if not isinstance(longitude, float):
            raise TypeError("Longitude must be a float")
        if longitude < -180 or longitude > 180:
            raise ValueError("Longitude must be between the range -180 and 180")
        
    def validate_latitude(self, latitude):
        if not isinstance(latitude, float):
            raise TypeError("Latitude must be a float")
        if latitude < -90 or latitude > 90:
            raise ValueError("Latitude must be between the range -90 and 90")
