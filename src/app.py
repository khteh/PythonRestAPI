"""
This script runs the application using a development server.
It contains the definition of routes and views for the application.
"""
from flask import Flask
from flask import request
from datetime import datetime
from config import app_config
from controllers.UserController import user_api as user_blueprint
from controllers.BlogController import blog_api as blog_blueprint
from controllers.GreetingController import greeting_api as greeting_blueprint
from controllers.FibonacciController import fibonacci_api as fibonacci_blueprint

# Make the WSGI interface available at the top level so wfastcgi can get it.
def create_app(env_name) -> Flask:
    """
    Create App
    """
    # App initialization
    app = Flask(__name__)
    app.config.from_object(app_config[env_name])
    wsgi_app = app.wsgi_app
    app.register_blueprint(greeting_blueprint, url_prefix="/api/v1/greeting")
    app.register_blueprint(fibonacci_blueprint, url_prefix="/api/v1/fibonacci")
    app.register_blueprint(user_blueprint, url_prefix="/api/v1/users")
    app.register_blueprint(blog_blueprint, url_prefix="/api/v1/blogs")
    return app