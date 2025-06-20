from base_class import BaseModel

class User(BaseModel):
    def __init__(self, id: str, first_name: str, last_name: str, email: str, is_admin, created_at, updated_at):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.is_admin = is_admin = False

        def validate_firts_name(self, first_name: str):
            if not isinstance(first_name, str):
                raise TypeError("Firts name mustb be a string")
            if first_name >= 50:
                raise ValueError("Maximum length is 50 characters")
            
        def validate_last_name(self, last_name: str):
            if not isinstance(last_name, str):
                raise TypeError("Last name must be a string")
