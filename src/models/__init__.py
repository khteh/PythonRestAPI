from flask_sqlalchemy import SQLAlchemy
from quart_bcrypt import Bcrypt
db = SQLAlchemy()
bcrypt = Bcrypt()
from .AuthorModel import AuthorModel, AuthorSchema
from .BookModel import BookModel, BookSchema
from .UserModel import UserModel, UserSchema
LibraryMetadata = db.Model.metadata