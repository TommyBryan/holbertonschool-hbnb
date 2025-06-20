import uuid
from datetime import datetime

class BaseModel:
    def __init__(self, id, created_at, updated_at):
        self.id = str(uuid.uuid4())
        self.created_at = datetime.now()
        self.updated_at = datetime.now()

    def save(self):
        """ Update the updated_at timestamp when object is modified """
        self.updated_at = datetime.now()

    def update(self, data):
        """ Update the attributes of the obj based on the provided data """
        for key, value in data.items():
            if hasattr(self, key):
                setattr(self, key, value)
        self.save()
