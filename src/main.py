import os
from dotenv import load_dotenv
from .app import create_app
from .models import db, bcrypt
load_dotenv()
if __name__ == '__main__':
    HOST = os.environ.get('SERVER_HOST', 'localhost')
    try:
        PORT = int(os.environ.get('SERVER_PORT', '5555'))
    except ValueError:
        PORT = 5555
    env_name = os.getenv('ENV', "Please set ENV in .env")
    print(f"env_name: {env_name}, __name__: {__name__}")
    app = create_app(env_name)
    bcrypt.init_app(app)
    db.init_app(app)
    app.run(HOST, PORT)