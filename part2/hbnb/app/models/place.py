from app.models.base_model import BaseModel
from app.models.user import User

class Place(BaseModel):
    def __init__(self, title, description="", price=0.0, latitude=0.0, longitude=0.0, owner=None, **kwargs):
        super().__init__(**kwargs)
        self.title = title[:100]  # Ensure title does not exceed 100 characters
        self.description = description
        self.price = max(0.0, price)  # Ensure price is a positive value
        self.latitude = max(-90.0, min(90.0, latitude))  # Ensure latitude is within range
        self.longitude = max(-180.0, min(180.0, longitude))  # Ensure longitude is within range
        self.owner = owner if isinstance(owner, User) else None  # Validate owner

    def __str__(self):
        return f"Place(id={self.id}, title={self.title}, price=${self.price}, owner={self.owner})"
