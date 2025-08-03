#!/usr/bin/python3
from app import db
from .base_class import BaseModel


class Amenity(BaseModel):
    """Represents an amenity that can be associated with a place."""
    __tablename__ = 'amenities'

    name = db.Column(db.String(100), nullable=False, unique=True)

    #Relationship
    places = db.relationship('Place', secondary='place_amenity', back_populates='amenities')

    def __init__(self, name):
        super().__init__()
        self.name = name.strip()
