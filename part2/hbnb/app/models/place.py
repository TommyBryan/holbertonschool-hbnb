from app.models.base_model import BaseModel

class Place(BaseModel):
    def __init__(self, name, location, price, **kwargs):
        super().__init__(**kwargs)
        self.name = name
        self.location = location
        self.price = price # Store price as a number (float)

    def __str__(self):
        return f"Place(name={self.name}, location={self.location}, price=${self.price})"
