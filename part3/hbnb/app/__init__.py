from flask import Flask
from flask_restx import Api
from app.api.v1.users import api as users_ns
from app.api.v1.amenities import api as amenities_ns
from app.api.v1.places import api as places_ns
from app.api.v1.reviews import api as reviews_ns
from app.extensions import bcrypt
from app.extensions import JWTManager

def create_app(config_class="config.DevelopmentConfig"):
    """
     Create and configure the Flask application.

    Returns:
        Flask: The configured Flask application instance.
    """
    app = Flask(__name__) 
    bcrypt.init_app(app)

    api = Api(
        app,
        version='1.0',
        title='HBnB API',
        description='HBnB Application API',
        doc='/api/v1/'
    )

    # Register the users namespace
    api.add_namespace(users_ns, path='/api/v1/users')
    return app
