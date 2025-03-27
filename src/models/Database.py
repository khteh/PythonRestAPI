import os, json
from urllib import parse
import sqlalchemy
from quart_sqlalchemy import SQLAlchemyConfig
from quart_sqlalchemy.framework import QuartSQLAlchemy
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