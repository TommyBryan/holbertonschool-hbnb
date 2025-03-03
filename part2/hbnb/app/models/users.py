from app.models.base import BaseModel

class User(BaseModel):
    def __init__(self, username, email, password, **kwargs):
        super().__init__(**kwargs) # Initialize BaseModel attributes
        self.username = username
        self.email = email
        self.password = password # NOTE: In production still

    def to_dict(self):
        """ Converts user object to dictionary but exclude sensitive data like passwords."""
        user_dict = super().to_dict()
        del user_dict['password'] # Exclude password for security reasons
        return user_dict
