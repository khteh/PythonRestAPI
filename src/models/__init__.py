import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from ..config import app_config
db = SQLAlchemy()
bcrypt = Bcrypt()
from .AuthorModel import AuthorModel, AuthorSchema
from .BookModel import BookModel, BookSchema
from .UserModel import UserModel, UserSchema