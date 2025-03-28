import os, json, sqlalchemy
from urllib import parse
from dotenv import load_dotenv
from quart_sqlalchemy import SQLAlchemyConfig
from quart_sqlalchemy.framework import QuartSQLAlchemy
load_dotenv()
if "Testing" in os.environ:
    connection_string = f"postgresql+psycopg://{os.environ.get('POSTGRESQL_USER')}:{parse.quote_plus(os.environ.get('POSTGRESQL_PASSWORD'))}@localhost:5432/library"
else:
    with open('/etc/pythonrestapi_config.json', 'r') as f:
        config = json.load(f)
    connection_string = f"postgresql+psycopg://{os.environ.get('DB_USERNAME')}:{parse.quote_plus(os.environ.get('DB_PASSWORD'))}@{config['DB_HOST']}/library"
db = QuartSQLAlchemy(
  config = SQLAlchemyConfig(
      binds = dict(
          default = dict(
              engine = dict(
                  url = connection_string,
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
engine = sqlalchemy.create_engine(connection_string, echo=False)