import os
from dotenv import load_dotenv
load_dotenv()

class Development(object):
    """
    Development environment configuration
    """
    DEBUG = True
    TESTING = False
    SECRET_KEY = os.environ.get("SECRET_KEY") or "you-will-never-guess"
    SQLALCHEMY_DATABASE_URI = f"mysql://{os.environ.get('MYSQL_USER')}:{os.environ.get('MYSQL_PASSWORD')}@svc-mysql/libarary"
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")
    OIDC_CLIENT_SECRETS = "manifests/oidc-secret.json"

class Production(object):
    """
    Production environment configuration
    """
    DEBUG = False
    TESTING = False
    SQLALCHEMY_DATABASE_URI = f"mysql://{os.environ.get('MYSQL_USER')}:{os.environ.get('MYSQL_PASSWORD')}@svc-mysql/libarary"
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL")
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")
    OIDC_CLIENT_SECRETS = "manifests/oidc-secret.json"

app_config = {
    "development": Development,
    "production": Production,
}
