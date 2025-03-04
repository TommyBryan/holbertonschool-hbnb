from app.models.base_model import BaseModel

class Review(BaseModel):
    def __init__(self, text: str, rating: int, place, user):
        super().__init__()
        self.text = text
        self.rating = self.validate_rating(rating)
        self.place = self.validate_place(place)
        self.user = self.validate_user(user)

    def validate_rating(self, rating):
        if not (1 <= rating <= 5):
            raise ValueError("Rating must be between 1 and 5")
        return rating

    def validate_place(self, place):
        if not isinstance(place, Place):
            raise ValueError("Place must be a Place instance")
        return place

    def validate_user(self, user):
        if not isinstance(user, User):
            raise ValueError("User must be a User instance")
        return user
