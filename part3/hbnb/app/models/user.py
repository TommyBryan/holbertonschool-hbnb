from app.models.base_class import BaseModel
import re
from app import db, bcrypt
from sqlalchemy.ext.hybrid import hybrid_property

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
    password = db.Column(db.String(128), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)

    @hybrid_property
    def password(self):
        raise AttributeError("Password is write-only.")

    @password.setter
    def password(self, password):
        self.hash_password(password)

    # This function takes a plaintext password and hashes it using bcrypt, and store the
    # hashed version in the password attribute.
    def hash_password(self, password):
        """Hashes the password before storing it."""
        self._password = bcrypt.generate_password_hash(password).decode('utf-8')

    # This function compares a plaintext password with the hashed password stored in the _password attribute.
    # It returns True if they match, otherwise False.
    def verify_password(self, password):
        """Verifies if the provided password matches the hashed password."""
        return bcrypt.check_password_hash(self._password, password)

    @property
    def places(self):
        """
        Get the list of places associated with the user.
        
        Returns:
            list: List of Place objects.
        """
        return self._places

    @places.setter
    def places(self, places):
        if not isinstance(places, list):
            raise TypeError("Places must be a list")
        # Avoid import issues by not checking Place type here
        self._places = places

    def add_place(self, place):
        """
        Add a place to the user's list of places.
        
        Args:
            place (Place): The place to add.
        """
        # Avoid import issues by not checking Place type here
        self._places.append(place)

    @property
    def first_name(self):
        """
        Get the first name of the user.
        
        Returns:
            str: First name of the user.
        """
        return self._first_name

    @first_name.setter
    def first_name(self, first_name):
        if not isinstance(first_name, str):
            raise TypeError("First name must be a string")
        if len(first_name) > 50:
            raise ValueError("Maximum length for first name is 50 characters")
        self._first_name = first_name

    @property
    def last_name(self):
        return self._last_name
    
    @last_name.setter
    def last_name(self, last_name):
        if not isinstance(last_name, str):
            raise TypeError("Last name must be a string")
        if len(last_name) > 50:
            raise ValueError("Maximum length for last name is 50 characters")
        self._last_name = last_name

    @property
    def email(self):
        return self._email
    
    @email.setter
    def email(self, email):
        if not isinstance(email, str):
            raise TypeError("Email must be a string")
        email_regex = r"^[\w\.-]+@[\w\.-]+\.\w+$"
        if not re.match(email_regex, email):
            raise ValueError("Invalid email format")
        self._email = email

    @property
    def is_admin(self):
        return self._is_admin
        # Uniqueness check should be handled at a higher level (e.g., database)
        self._email = email

    @property
    def is_admin(self):
        return self._is_admin
