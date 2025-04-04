import logging, os, asyncio, json
from datetime import date, datetime, timedelta, timezone
from urllib import parse
from hypercorn.config import Config
from hypercorn.middleware import HTTPToHTTPSRedirectMiddleware
from quart import Quart, Response, request
from quart_trio import QuartTrio
from quart_wtf.csrf import CSRFProtect
from quart_cors import cors
from psycopg import Error
from src.controllers.AuthenticationController import auth_api as auth_blueprint
from src.controllers.UserController import user_api as user_blueprint
from src.controllers.AuthorController import author_api as author_blueprint
from src.controllers.BookController import book_api as book_blueprint
from src.controllers.HomeController import home_api as home_blueprint
from src.controllers.FibonacciController import fibonacci_api as fibonacci_blueprint
from src.controllers.HealthController import health_api as health_blueprint
from src.models.Database import db
from src.common.Bcrypt import bcrypt
from src.common.ResponseHelper import Respond
from src.config import config as appconfig
config = Config()
config.from_toml("/etc/hypercorn.toml")

def _add_secure_headers(response: Response) -> Response:
    response.headers["Strict-Transport-Security"] = (
        "max-age=63072000; includeSubDomains; preload"
    )
    response.headers["X-Content-Type-Options"] = "nosniff"
    return response

def create_app() -> Quart:
    """
    Create App
    """
    # App initialization
    app = Quart(__name__, template_folder='view/templates', static_url_path='', static_folder='view/static')
    app.config.from_file("/etc/pythonrestapi_config.json", json.load)
    app.config["SEND_FILE_MAX_AGE_DEFAULT"] = timedelta(days=90)
    app.config["SQLALCHEMY_DATABASE_URI"] = f"postgresql+psycopg://{os.environ.get('DB_USERNAME')}:{parse.quote_plus(os.environ.get('DB_PASSWORD'))}@{app.config['DB_HOST']}/library"
    app.config["POSTGRESQL_DATABASE_URI"] = f"postgresql://{os.environ.get('DB_USERNAME')}:{parse.quote_plus(os.environ.get('DB_PASSWORD'))}@{app.config['DB_HOST']}/library"
    app.config["TEMPLATES_AUTO_RELOAD"] = True
    app.after_request(_add_secure_headers)
    app.register_blueprint(home_blueprint, url_prefix="/")
    app.register_blueprint(health_blueprint, url_prefix="/health")
    app.register_blueprint(fibonacci_blueprint, url_prefix="/fibonacci")
    app.register_blueprint(auth_blueprint, url_prefix="/auth")
    app.register_blueprint(user_blueprint, url_prefix="/users")
    app.register_blueprint(author_blueprint, url_prefix="/authors")
    app.register_blueprint(book_blueprint, url_prefix="/books")
    app = cors(app, allow_credentials=True, allow_origin="https://localhost")
    # https://quart-wtf.readthedocs.io/en/stable/how_to_guides/configuration.html
    csrf = CSRFProtect(app)
    bcrypt.init_app(app)
    db.init_app(app)
    # https://hypercorn.readthedocs.io/en/stable/how_to_guides/http_https_redirect.html
    #return HTTPToHTTPSRedirectMiddleware(app, "khteh.com")  # type: ignore - Defined in hypercorn.toml server_names
    return app

#app = asyncio.get_event_loop().run_until_complete(create_app())
app = create_app()
logging.info(f"Running app...")
#asyncio.run(serve(app, config), debug=True)