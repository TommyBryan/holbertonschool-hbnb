from app.models.base_class import BaseModel
import re
from app import db, bcrypt
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import validates

class User(BaseModel):
    """
    User model class that inherits from BaseModel.

    Represents a user with first name, last name, email, password, and admin status.
    Handles password hashing and validation, and maintains a relationship with Place instances.
    """
    __tablename__ = 'users'

    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True)
    _password = db.Column('password', db.String(128), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)

    # SQLAlchemy validators
    @validates('first_name')
    def validate_first_name(self, key, first_name):
        if not isinstance(first_name, str):
            raise TypeError("First name must be a string")
        if len(first_name) > 50:
            raise ValueError("Maximum length for first name is 50 characters")
        return first_name

    @validates('last_name')
    def validate_last_name(self, key, last_name):
        if not isinstance(last_name, str):
            raise TypeError("Last name must be a string")
        if len(last_name) > 50:
            raise ValueError("Maximum length for last name is 50 characters")
        return last_name

    @validates('email')
    def validate_email(self, key, email):
        if not isinstance(email, str):
            raise TypeError("Email must be a string")
        email_regex = r"^[\w\.-]+@[\w\.-]+\.\w+$"
        if not re.match(email_regex, email):
            raise ValueError("Invalid email format")
        return email

    @hybrid_property
    def password(self):
        raise AttributeError("Password is write-only.")

    @password.setter
    def password(self, password):
        self.hash_password(password)

    def hash_password(self, password):
        """Hashes the password before storing it."""
        self._password = bcrypt.generate_password_hash(password).decode('utf-8')

    def verify_password(self, password):
        """Verifies if the provided password matches the hashed password."""
        return bcrypt.check_password_hash(self._password, password)

    # Keep custom properties only for attributes that aren't SQLAlchemy columns
    @property
    def places(self):
        """Get the list of places associated with the user."""
        return getattr(self, '_places', [])

    @places.setter
    def places(self, places):
        if not isinstance(places, list):
            raise TypeError("Places must be a list")
        self._places = places

    def add_place(self, place):
        """Add a place to the user's list of places."""
        if not hasattr(self, '_places'):
            self._places = []
        self._places.append(place)
