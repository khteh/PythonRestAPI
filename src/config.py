import os, json
from dotenv import load_dotenv
from urllib import parse
load_dotenv()
class Config:
    DEBUG = False
    TESTING = False
    with open('/etc/pythonrestapi_config.json', 'r') as f:
        config = json.load(f)
    SECRET_KEY = config["SECRET_KEY"] or "you-will-never-guess"
    SQLALCHEMY_DATABASE_URI = f"postgresql+psycopg://{os.environ.get('DB_USERNAME')}:{parse.quote_plus(os.environ.get('DB_PASSWORD'))}@{config['DB_HOST']}/library"
    POSTGRESQL_DATABASE_URI = f"postgresql://{os.environ.get('DB_USERNAME')}:{parse.quote_plus(os.environ.get('DB_PASSWORD'))}@{config['DB_HOST']}/library"
    JWT_SECRET_KEY = config["JWT_SECRET_KEY"]
