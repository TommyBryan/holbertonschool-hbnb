from app.models.base_class import BaseModel

class Amenity(BaseModel):
    def __init__(self, name):
        super().__init__()
        self.validate_name(name)
        self.name = name

    def validate_name(self, name):
        if not isinstance(name, str):
            raise TypeError("Name must be a string")
        if len(name) > 50:
            raise ValueError("Maximum length is 50 characters")
