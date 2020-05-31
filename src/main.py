import os
from app import create_app
from models import db, bcrypt
if __name__ == '__main__':
    HOST = os.environ.get('SERVER_HOST', 'localhost')
    try:
        PORT = int(os.environ.get('SERVER_PORT', '5555'))
    except ValueError:
        PORT = 5555
    env_name = os.getenv('FLASK_ENV', "Please set FLASK_ENV")
    print("env_name: ", env_name)
    app = create_app(env_name)
    bcrypt.init_app(app)
    db.init_app(app)
    app.run(HOST, PORT)