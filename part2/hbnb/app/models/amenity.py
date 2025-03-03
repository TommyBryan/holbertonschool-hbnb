from app.models.base_model import BaseModel

class Amenity(BaseModel):
    def __init__(self, name, description, **kwargs):
        super().__init__(**kwargs)
        self.name = name
        self.description = description

    def __str__(self):
        return f"Amenity(name={self.name}, description={self.description})"
