from app.models.base_class import BaseModel


class Review(BaseModel):
    def __init__(self, text, rating, place, user):
        super().__init__()
        self.text = text
        self.rating = rating
        self.place = place
        self._user = user

    @property
    def text(self):
        return self._text
    
    @text.setter
    def text(self, text):
        if not isinstance(text, str):
            raise TypeError("Text must be a string")
        if len(text) < 1:
            raise ValueError("Text cannot be empty")
        self._text = text

    @property
    def rating(self):
        return self._rating
    
    @rating.setter
    def rating(self, rating):
        if not isinstance(rating, int):
            raise TypeError("Rating must be an integer")
        if rating < 1 or rating > 5:
            raise ValueError("Must be between 1 and 5")
        self._rating = rating

    @property
    def place(self):
        return self._place
    
    @place.setter
    def place(self, place):
        from .place import Place
        if not isinstance(place, Place):
            raise ValueError("Place does not exist")
        self._place = place

    @property
    def user(self):
        return self._user
    
    @user.setter
    def user(self, user):
        from .user import User
        if not isinstance(user, User):
            raise ValueError("User does not exist")
        self._user = user
