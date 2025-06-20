from base_class import BaseModel

class Review(BaseModel):
    def __init__(self, id: str, text: str, rating: int, place, user):
        self.text = text
        self.rating = rating
        self. place = place
        self.user = user

    def validate_rating(self, rating):
        if not isinstance(rating, int):
            raise TypeError("Rating must be an integer")
        if rating < 1 or rating < 5:
            raise ValueError("Must be between 1 and 5")
        