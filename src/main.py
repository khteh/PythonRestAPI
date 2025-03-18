import quart_flask_patch
import logging, os, asyncio
from urllib import parse
from hypercorn.config import Config
import quart_flask_patch, json, logging, os
from quart import Quart, request
from flask_healthz import Healthz, HealthError
from quart_wtf.csrf import CSRFProtect
from quart_cors import cors
from psycopg import Error
from psycopg_pool import AsyncConnectionPool, ConnectionPool
from src.controllers.AuthenticationController import auth_api as auth_blueprint
from src.controllers.UserController import user_api as user_blueprint
from src.controllers.AuthorController import author_api as author_blueprint
from src.controllers.BookController import book_api as book_blueprint
from src.controllers.HomeController import home_api as home_blueprint
from src.controllers.FibonacciController import fibonacci_api as fibonacci_blueprint
from src.models import db, bcrypt
config = Config()
config.from_toml("/etc/hypercorn.toml")
logging.basicConfig(format='%(asctime)s %(levelname)-8s %(message)s', level=logging.INFO, datefmt='%Y-%m-%d %H:%M:%S')	
#oidc.init_app(app)

def create_app() -> Quart:
    """
    Create App
    """
    # App initialization
    app = Quart(__name__, template_folder='view/templates', static_url_path='', static_folder='view/static')
    app.config.from_file("/etc/pythonrestapi_config.json", json.load)
    if "SQLALCHEMY_DATABASE_URI" not in app.config:
        app.config["SQLALCHEMY_DATABASE_URI"] = f"postgresql+psycopg://{os.environ.get('DB_USERNAME')}:{parse.quote(os.environ.get('DB_PASSWORD'))}@{app.config['DB_HOST']}/library"
        app.config["POSTGRESQL_DATABASE_URI"] = f"postgresql://{os.environ.get('DB_USERNAME')}:{parse.quote(os.environ.get('DB_PASSWORD'))}@{app.config['DB_HOST']}/library"
    app.register_blueprint(home_blueprint, url_prefix="/")
    app.register_blueprint(fibonacci_blueprint, url_prefix="/fibonacci")
    app.register_blueprint(auth_blueprint, url_prefix="/auth")
    app.register_blueprint(user_blueprint, url_prefix="/users")
    app.register_blueprint(author_blueprint, url_prefix="/authors")
    app.register_blueprint(book_blueprint, url_prefix="/books")
    app = cors(app, allow_credentials=True, allow_origin="https://localhost:4433")
    print(f"HEALTHZ: {app.config['HEALTHZ']}")
    Healthz(app, no_log=False)
    # https://quart-wtf.readthedocs.io/en/stable/how_to_guides/configuration.html
    csrf = CSRFProtect(app)
    bcrypt.init_app(app)
    db.init_app(app)
    return app

def liveness():
    print("Alive!")
    pass 

def readiness():
    try:
        print(f"readiness {app.config["POSTGRESQL_DATABASE_URI"]}")
        connection_kwargs = {
            "autocommit": True,
            "prepare_threshold": 0,
        }
        with ConnectionPool(
            conninfo = app.config["POSTGRESQL_DATABASE_URI"],
            max_size = app.config["DB_MAX_CONNECTIONS"],
            kwargs = connection_kwargs,
        ) as pool:
            # Check if the checkpoints table exists
            with pool.connection() as conn:
                with conn.cursor() as cur:
                    try:
                        cur.execute("""
                            SELECT EXISTS (
                                SELECT FROM information_schema.tables 
                                WHERE  table_schema = 'public'
                                AND    table_name   = 'library'
                            );
                        """)
                    except Error as e:
                        raise HealthError(f"Error checking for library table: {e}")
                        # Optionally, you might want to raise this error
                        # raise
        print("Ready!")
    except Exception:
        raise HealthError(f"Failed to connect to the database! {app.config['POSTGRESQL_DATABASE_URI']}")

app = create_app()
print(f"Running asyncio...")
#asyncio.run(serve(app, config), debug=True)