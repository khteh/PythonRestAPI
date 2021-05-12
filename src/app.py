"""
This script runs the application using a development server.
It contains the definition of routes and views for the application.
"""
from flask import Flask, request
from flask_healthz import healthz, HealthError
from datetime import datetime
from .config import app_config
from .controllers.AuthenticationController import auth_api as auth_blueprint
from .controllers.UserController import user_api as user_blueprint
from .controllers.AuthorController import author_api as author_blueprint
from .controllers.BookController import book_api as book_blueprint
from .controllers.HomeController import home_api as home_blueprint
from .controllers.FibonacciController import fibonacci_api as fibonacci_blueprint
from .models import db, bcrypt
# Make the WSGI interface available at the top level so wfastcgi can get it.
def create_app(env_name) -> Flask:
    """
    Create App
    """
    # App initialization
    app = Flask(__name__, template_folder='view/templates', static_url_path='', static_folder='view/static')
    app.config.from_object(app_config[env_name])
    # initializing bcrypt
    bcrypt.init_app(app)
    db.init_app(app)
    wsgi_app = app.wsgi_app
    app.register_blueprint(home_blueprint, url_prefix="/")
    app.register_blueprint(healthz, url_prefix="/healthz")
    app.register_blueprint(fibonacci_blueprint, url_prefix="/fibonacci")
    app.register_blueprint(auth_blueprint, url_prefix="/auth")
    app.register_blueprint(user_blueprint, url_prefix="/users")
    app.register_blueprint(author_blueprint, url_prefix="/authors")
    app.register_blueprint(book_blueprint, url_prefix="/books")
    return app

def liveness():
    pass

def readiness():
    try:
        db.engine.execute('select 1')
    except Exception:
        raise HealthError(f"Failed to connect to the database!")
