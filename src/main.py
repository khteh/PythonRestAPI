import quart_flask_patch
import logging, os, re
from hypercorn.config import Config
import asyncio
from hypercorn.asyncio import serve
from src.app import create_app
from src.models import bcrypt, db
config = Config()
config.from_toml("/etc/hypercorn.toml")
app = create_app()
logging.basicConfig(format='%(asctime)s %(levelname)-8s %(message)s', level=logging.INFO, datefmt='%Y-%m-%d %H:%M:%S')	
#oidc.init_app(app)

#app.run(HOST, PORT)
print(f"Running asyncio...")
#asyncio.run(serve(app, config), debug=True)