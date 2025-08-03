from app import db
import uuid
from datetime import datetime

class BaseModel(db.Model):
    """
    Base model class that provides common attributes and methods for other models.
    
    Attributes:
        id (str): Primary key, a UUID string.
        created_at (datetime): Timestamp when the instance was created.
        updated_at (datetime): Timestamp when the instance was last updated.
    """
    __abstract__ = True  # This ensures SQLAlchemy does not create a table for BaseModel

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __init__(self):
        pass

    def save(self):
        """ Update the updated_at timestamp when object is modified """
        self.updated_at = datetime.now()

    def update(self, data):
        """ Update the attributes of the obj based on the provided data """
        for key, value in data.items():
            if hasattr(self, key):
                setattr(self, key, value)
        self.save()
