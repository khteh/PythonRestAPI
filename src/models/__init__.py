from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
db = SQLAlchemy()
bcrypt = Bcrypt()
from .BlogModel import BlogModel, BlogSchema
from .UserModel import UserModel, UserSchema