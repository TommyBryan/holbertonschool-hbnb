from app.models.base_model import BaseModel

class Review(BaseModel):
    def __init__(self, text, rating, place, user):
        super().__init__()
        self.text = text
        self.rating = rating
        self.place = place
        self.user = user

        self.validate_rating()

    def validate_rating(self):
        if not (1 <= self.rating <= 5):
            raise ValueError("Rating must be between 1 and 5")

    def set_place(self, place):
        """Set the place for the review."""
        self.place = place

    def set_user(self, user):



        self.user = user        """Set the user for the review."""
