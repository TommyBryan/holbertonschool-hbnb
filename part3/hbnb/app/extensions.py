from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager

"""This file contains all the extensions to run the Flask app"""

db = SQLAlchemy()
bcrypt = Bcrypt()
jwt = JWTManager()
