from datetime import datetime
from sqlalchemy import Integer, String, DateTime
from marshmallow import fields, Schema
from sqlalchemy.sql import func
import sqlalchemy as sa
import sqlalchemy.orm
from sqlalchemy.orm import Mapped, mapped_column
from quart import Quart
from quart_sqlalchemy import SQLAlchemyConfig
from quart_sqlalchemy.framework import QuartSQLAlchemy
from src.common.Bcrypt import bcrypt
from .base import Base
from .Database import db
from .BookModel import BookSchema
class UserModel(Base):
    """
    User Model
    """
    __tablename__ = 'users'
    id: Mapped[int] = mapped_column(sa.Identity(), primary_key=True, autoincrement=True)
    firstname: Mapped[str] = mapped_column(sa.String(128), nullable=False)
    lastname: Mapped[str] = mapped_column(sa.String(128), nullable=False)
    email: Mapped[str] = mapped_column(sa.String(255), unique=True, nullable=False, index=True)
    phone: Mapped[str] = mapped_column(sa.String(15), unique=True, nullable=True, index=True)
    password: Mapped[str] = mapped_column(sa.String(128), nullable=True)
    lastlogin: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=sa.func.now(),
        server_default=sa.FetchedValue(),
        nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=sa.func.now(),
        server_default=sa.FetchedValue()
    )
    modified_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=sa.func.now(),
        onupdate=sa.func.now(),
        server_default=sa.FetchedValue(),
        server_onupdate=sa.FetchedValue()
    )
    # Class constructor
    def __init__(self, data):
        """
        Class Constructor
        """
        self.firstname = data.get("firstname")
        self.lastname = data.get("lastname")
        self.email = data.get("email")
        self.phone = data.get("phone")
        self.password = self.__generate_hash(data.get("password"))
        self.created_at = func.now()
        self.modified_at = func.now()
    def save(self):
        db.session.add(self)
        db.session.commit()
    def update(self, data):
        for key, value in data.items():
            if key == "password":
                value = self.__generate_hash(value)
            setattr(self, key, value)
        self.modified_at = func.now()
        db.session.commit()
    def delete(self):
        db.session.delete(self)
        db.session.commit()
    def __generate_hash(self, password):
        return bcrypt.generate_password_hash(password, rounds=10).decode("utf-8")
    def check_hash(self, password):
        return bcrypt.check_password_hash(self.password, password)
    @staticmethod
    def get_user(id):
        return UserModel.query.get(id)
    @staticmethod
    def get_user_by_email(email):
        return UserModel.query.filter_by(email=email).first()
    @staticmethod
    def isExistingUser(email):
        return UserModel.query.filter_by(email = email).count() > 0
    @staticmethod
    def get_users():
        return UserModel.query.all()
    def __repl__(self): # return a printable representation of UserModel object, in this case we're only returning the id
        return "<id {}>".format(self.id)
class UserSchema(Schema):
    """
    User Schema
    """
    id = fields.Int(dump_only=True)
    firstname = fields.Str(required=True)
    lastname = fields.Str(required=True)
    email = fields.Email(required=True)
    phone = fields.Str(required=False)
    password = fields.Str(required=True)
    lastlogin = fields.DateTime(required=False)
    created_at = fields.DateTime(dump_only=True)
    modified_at = fields.DateTime(dump_only=True)