import os, json
from dotenv import load_dotenv
from urllib import parse
load_dotenv()
"""
class Development(object):
    DEBUG = True
    TESTING = False
    SECRET_KEY = os.environ.get("SECRET_KEY") or "you-will-never-guess"
    SQLALCHEMY_DATABASE_URI = f"postgresql://{os.environ.get('POSTGRESQL_USER')}:{os.environ.get('POSTGRESQL_PASSWORD')}@svc-postgresql/library"
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")
    OIDC_CLIENT_SECRETS = "manifests/oidc-secret.json"

class Production(object):
    DEBUG = False
    TESTING = False
    SQLALCHEMY_DATABASE_URI = f"postgresql://{os.environ.get('POSTGRESQL_USER')}:{os.environ.get('POSTGRESQL_PASSWORD')}@svc-postgresql/library"
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")
    OIDC_CLIENT_SECRETS = "manifests/oidc-secret.json"

app_config = {
    "development": Development,
    "production": Production,
}
"""
class Config:
    DEBUG = False
    TESTING = False
    with open('/etc/pythonrestapi_config.json', 'r') as f:
        config = json.load(f)
    SECRET_KEY = config["SECRET_KEY"] or "you-will-never-guess"
    SQLALCHEMY_DATABASE_URI = f"postgresql+psycopg://{os.environ.get('DB_USERNAME')}:{parse.quote(os.environ.get('DB_PASSWORD'))}@{config['DB_HOST']}/library"
    POSTGRESQL_DATABASE_URI = f"postgresql://{os.environ.get('DB_USERNAME')}:{parse.quote(os.environ.get('DB_PASSWORD'))}@{config['DB_HOST']}/library"
    JWT_SECRET_KEY = config["JWT_SECRET_KEY"]
    OIDC_CLIENT_SECRETS = config["OIDC_CLIENT_SECRETS"]