import os, json, sqlalchemy
from dotenv import load_dotenv
from urllib import parse
from quart_sqlalchemy import SQLAlchemyConfig
from quart_sqlalchemy.framework import QuartSQLAlchemy
from src.config import config
load_dotenv()
#connection_string = f"postgresql+psycopg://{os.environ.get('DB_USERNAME')}:{parse.quote_plus(os.environ.get('DB_PASSWORD'))}@{config['DB_HOST']}:5432/library" if "Testing" in os.environ else config.SQLALCHEMY_DATABASE_URI
db = QuartSQLAlchemy(
  config = SQLAlchemyConfig(
      binds = dict(
          default = dict(
              engine = dict(
                  url = config.SQLALCHEMY_DATABASE_URI,
                  echo = True,
                  connect_args = dict(check_same_thread=False),
              ),
              session=dict(
                  expire_on_commit=False,
              ),
          )
      )
  )
)
engine = sqlalchemy.create_engine(config.SQLALCHEMY_DATABASE_URI, echo=False)