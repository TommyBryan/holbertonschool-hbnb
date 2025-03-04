from app.models.base_model import BaseModel

class Amenity(BaseModel):
    def __init__(self, name):
        super().__init__()
        self.name = name
        
        self.validate_name()
        
    def validate_name(self):
        if len(self.name) > 50:
            raise ValueError("Name cannot exceed 50 characters")
        
    def __str__(self):
        return f"Amenity(name={self.name})"
