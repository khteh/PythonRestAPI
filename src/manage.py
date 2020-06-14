import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from src.config import app_config
from src.app import create_app, db
from dotenv import load_dotenv
load_dotenv()
env_name = os.getenv("ENV")
print(f"env_name: {env_name}, __name__: {__name__}, ")
app = create_app(env_name)
dbConnetionSring = app.config.get("SQLALCHEMY_DATABASE_URI")
print(f"SQLALCHEMY_DATABASE_URI: {dbConnetionSring}")
migrate = Migrate(app=app, db=db)
manager = Manager(app=app)
manager.add_command("db", MigrateCommand)

if __name__ == "__main__":
    manager.run()