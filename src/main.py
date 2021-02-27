import os
from dotenv import load_dotenv
from .app import create_app
from .models import db, bcrypt
load_dotenv()
if __name__ == '__main__':
    HOST = os.environ.get('SERVER_HOST', '0.0.0.0')
    try:
        PORT = int(os.environ.get('SERVER_PORT', '8080'))
    except ValueError:
        PORT = 8080
    env_name = os.getenv('ENV', "Please set ENV in .env")
    print(f"env_name: {env_name}, __name__: {__name__}, {HOST}:{PORT}")
    app = create_app(env_name)
    bcrypt.init_app(app)
    db.init_app(app)
    app.run(HOST, PORT)