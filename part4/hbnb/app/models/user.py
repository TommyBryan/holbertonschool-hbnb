#!/usr/bin/python3
"""User Model"""
from app.extensions import db, bcrypt
from .base_class import BaseModel


class User(BaseModel):
    """"Defines a User with atrributes inherited from (SQLALCHEMY model)"""
    __tablename__ = 'users'  # Define the table name

    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True, index=True)
    password_hash = db.Column(db.String(128), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)

    places = db.relationship('Place', back_populates='owner', cascade="all, delete-orphan")
    reviews = db.relationship('Review', back_populates='user', cascade="all, delete-orphan")

    def __init__(self, first_name, last_name, email, password=None, is_admin=False):
        """Initialize a User instance"""
        super().__init__()
        self.first_name = self._validate_string(first_name, "First name")
        self.last_name = self._validate_string(last_name, "Last name")
        self.email = self._validate_email(email)
        self.is_admin = is_admin

        # Hash password if provided
        if password:
            self.hash_password(password)

    def hash_password(self, password):
        """Hashes the password before storing it."""
        self.password_hash = bcrypt.generate_password_hash(password).decode('utf-8')

    def verify_password(self, password):
        """Verifies if the provided password matches the hashed password."""
        return bcrypt.check_password_hash(self.password_hash, password)

    def to_dict(self):
        """Convert user to dictionary"""
        return {
            'id': self.id,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'email': self.email,
            'is_admin': self.is_admin,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
            # Note: password_hash is excluded for security
        }
