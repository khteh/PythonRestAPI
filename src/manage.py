import quart.flask_patch
from flask_migrate import Migrate
from src.app import create_app, db
from dotenv import load_dotenv
load_dotenv()
app = create_app()
print(f"SQLALCHEMY_DATABASE_URI: {app.config.get('SQLALCHEMY_DATABASE_URI')}")
migrate = Migrate(app=app, db=db)