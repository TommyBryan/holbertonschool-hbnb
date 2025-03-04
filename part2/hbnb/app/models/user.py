from app.models.base_model import BaseModel
import re

class User(BaseModel):
    def __init__(self, first_name: str, last_name: str, email: str, is_admin: bool = False):
        super().__init__()
        self.first_name = self.validate_name(first_name)
        self.last_name = self.validate_name(last_name)
        self.email = self.validate_email(email)
        self.is_admin = is_admin
        self.places = []  # List to store places owned by the user

    def validate_name(self, name):
        if not isinstance(name, str) or len(name) > 50:
            raise ValueError("Name must be a string with a maximum of 50 characters")
        return name
    
    def validate_email(self, email):
        email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
        if not re.match(email_regex, email):
            raise ValueError("Invalid email address")
        return email

    def add_place(self, place):
        """Add a place to the user's list of owned places."""
        self.places.append(place)

    def to_dict(self):
        """ Converts user object to dictionary but exclude sensitive data like passwords."""
        user_dict = super().to_dict()
        del user_dict['password'] # Exclude password for security reasons
        return user_dict
