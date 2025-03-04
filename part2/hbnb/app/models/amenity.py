from app.models.base_model import BaseModel

class Amenity(BaseModel):
    def __init__(self, name):
        super().__init__()
        self.name = self.validate_name(name)
        
    def validate_name(self, name):
        if len(name) > 50:
            raise ValueError("Name cannot exceed 50 characters")
        return name
        
    def __str__(self):
        return f"Amenity(name={self.name})"
