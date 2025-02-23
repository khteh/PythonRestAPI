import quart_flask_patch
import logging, os, re
from flask_healthz import Healthz
from quart_wtf.csrf import CSRFProtect
from quart_cors import cors
from hypercorn.config import Config
import asyncio
from hypercorn.asyncio import serve
from src.app import create_app
from src.models import bcrypt, db
config = Config()
#from .common.Authentication import oidc
config.from_toml("/etc/pythonrestapi.toml")
app = create_app()
app = cors(app, allow_credentials=True, allow_origin="https://localhost:4433")
Healthz(app, no_log=True)
csrf = CSRFProtect(app)
bcrypt.init_app(app)
logging.basicConfig(format='%(asctime)s %(levelname)-8s %(message)s', level=logging.INFO, datefmt='%Y-%m-%d %H:%M:%S')	
#oidc.init_app(app)

#app.run(HOST, PORT)
print(f"Running asyncio...")
asyncio.run(serve(app, config), debug=True)