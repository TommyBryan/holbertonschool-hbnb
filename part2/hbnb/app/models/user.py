from app.models.base_model import BaseModel

class User(BaseModel):
    def __init__(self, first_name, last_name, email, is_admin=False):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.is_admin = is_admin

    def to_dict(self):
        """ Converts user object to dictionary but exclude sensitive data like passwords."""
        user_dict = super().to_dict()
        del user_dict['password'] # Exclude password for security reasons
        return user_dict
