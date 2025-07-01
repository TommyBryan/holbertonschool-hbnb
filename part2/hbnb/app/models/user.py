from app.models.base_class import BaseModel
import re

class User(BaseModel):
    """
    User model cls inherits from BaseModel.
    """
    def __init__(self, first_name, last_name, email, is_admin=False):
        """
        Initialize a User instance.

        Args:
            first_name (str): The first name of the user.
            last_name (str): The last name of the user.
            email (str): The email of the user.
            is_admin (bool): The admin status of the user. Defaults to False.
        """
        super().__init__()
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.is_admin = is_admin
        self.places = []  # List to store related places

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
        for place in places:
            from place import Place
            if not isinstance(place, Place):
                raise TypeError("All items in places must be Place instances")
        self._places = places

    def add_place(self, place):
        """
        Add a place to the user's list of places.
        
        Args:
            place (Place): The place to add.
        """
        from place import Place
        if not isinstance(place, Place):
            raise TypeError("place must be a Place instance")
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
        # Uniqueness check should be handled at a higher level (e.g., database)
        self._email = email

    @property
    def is_admin(self):
        return self._is_admin
