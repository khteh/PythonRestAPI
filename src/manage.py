import os
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from app import create_app
from models import db
env_name = os.getenv("FLASK_ENV")
print("Using env {0}".format(env_name))
app = create_app(env_name)
migrate = Migrate(app=app, db=db)
manager = Manager(app=app)
manager.add_command("db", MigrateCommand)
if __name__ == "__main__":
    manager.run()