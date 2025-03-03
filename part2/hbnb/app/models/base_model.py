import uuid
from datetime import datetime

class BaseModel:
    def __init__(self, id=None, created_at=None,updated_at=None):
        self.id = id or str(uuid.uuid4()) # Generate a unique ID
        self.created_at = created_at or datetime.utcnow() # Creation timestamp
        self.updated_at = updated_at or datetime.utcnow() # Last updated timestamp

    def save(self):
        """ Updated the 'updated_at' timestamp whenever the object is saved. """
        self.updated_at = datetime.utcnow()

    def update(self, data):
        """ Update the object with the data provided. """
        for key, value in data.items():
            if hasattr(self, key):
                setattr(self, key, value)
        self.updated_at = datetime.utcnow()

    def to_dict(self):
        """ Convert object to dictionary format (for API responses)."""
        return self.__dict__.copy()
