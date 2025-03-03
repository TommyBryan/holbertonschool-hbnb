from app.models.base import BaseModel

class Review(BaseModel):
    def __init__(self, user_id, place_id, rating, comment, **kwargs):
        super().__init__(**kwargs)
        self.user_id = user_id # Refering to User
        self.place_id = place_id # Refering to Place
        self.rating = rating # Integer rating (1-5)
        self.comment = comment # Text review

    def __str__(self):
        return f"Review(user={self.user_id}, place={self.place_id}, rating={self.rating}, comment={self.comment})"
