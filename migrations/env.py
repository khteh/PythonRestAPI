# Copy this file to migrations/env.py
import os, sys, json, urllib
from dotenv import load_dotenv
from urllib import parse
from logging.config import fileConfig
from urllib.parse import unquote
from sqlalchemy import engine_from_config, pool, FetchedValue
from alembic import context
load_dotenv()
# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
f = open("/etc/pythonrestapi_config.json", "r")
json_config = json.load(f)
config = context.config

# Interpret the config file for Python logging.
# This line sets up loggers basically.
fileConfig(config.config_file_name)

# add your model's MetaData object here
# for 'autogenerate' support
# from myapp import mymodel
# target_metadata = mymodel.Base.metadata
from src.models.base import Base
from src.models.AuthorModel import AuthorModel
from src.models.BookModel import BookModel
from src.models.UserModel import UserModel

target_metadata = Base.metadata

#from src.models.Database import LibraryMetadata
#target_metadata = LibraryMetadata

# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.
section = config.config_ini_section
print(f"password: {os.environ.get('DB_PASSWORD')}, host: {json_config['DB_HOST']}, db: {json_config['DB_DATABASE']}")
config.set_section_option(section, "DB_USERNAME", os.environ.get('DB_USERNAME'))
config.set_section_option(section, "DB_PASSWORD", urllib.parse.quote_plus(os.environ.get('DB_PASSWORD')).replace("%", "%%"))
config.set_section_option(section, "DB_HOST", json_config["DB_HOST"])
config.set_section_option(section, "DB_DATABASE", json_config["DB_DATABASE"])
def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection, target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
