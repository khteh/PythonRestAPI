from datetime import datetime, timezone
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema, auto_field
from sqlalchemy import Integer, String, DateTime, select, func
from marshmallow import fields, Schema
from sqlalchemy.orm import Mapped, mapped_column
from src.common.Bcrypt import bcrypt
from .base import Base
from . import async_session
class UserModel(Base):
    """
    User Model
    https://marshmallow-sqlalchemy.readthedocs.io/en/latest/
    All database access is async (SQLAlchemy AsyncSession).
    """
    __tablename__ = 'users'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    firstname: Mapped[str] = mapped_column(String(128), nullable=False)
    lastname: Mapped[str] = mapped_column(String(128), nullable=False)
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False, index=True)
    phone: Mapped[str] = mapped_column(String(15), unique=True, nullable=True, index=True)
    password: Mapped[str] = mapped_column(String(128), nullable=True)
    lastlogin: Mapped[DateTime] = mapped_column(DateTime(timezone=True), nullable=True)
    created_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    modified_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    @classmethod
    def fromdata(cls, data):
        user = UserModel()
        user.firstname = data.firstname
        user.lastname = data.lastname
        user.email = data.email
        user.phone = data.phone
        user.password = user.__generate_hash(data.password)
        user.created_at = datetime.now(timezone.utc)
        user.modified_at = datetime.now(timezone.utc)
        return user
    async def save(self):
        async with async_session() as session:
            session.add(self)
            await session.commit()
    async def update(self, data):
        """data: dict or model instance. Only explicitly provided (non-private) attributes are applied."""
        values = dict(data) if isinstance(data, dict) else {k: v for k, v in vars(data).items() if not k.startswith("_")}
        if "password" in values:
            values["password"] = self.__generate_hash(values["password"])
        values["modified_at"] = datetime.now(timezone.utc)
        async with async_session() as session:
            user = await session.get(UserModel, self.id)
            for attribute, value in values.items():
                setattr(user, attribute, value)
            await session.commit()
            for attribute, value in values.items():
                setattr(self, attribute, value)
    async def delete(self):
        async with async_session() as session:
            user = await session.get(UserModel, self.id)
            if user:
                await session.delete(user)
                await session.commit()
    def __generate_hash(self, password):
        return bcrypt.generate_password_hash(password, rounds=10).decode("utf-8")
    def check_hash(self, password):
        return bcrypt.check_password_hash(self.password, password)
    @property
    def serialized(self):
        """Return object data in serializable format"""
        return {
            'id': self.id,
            'firstname': self.firstname,
            'lastname': self.lastname,
            'email': self.email,
            'phone': self.phone,
            'lastlogin': self.lastlogin,
            'created_at': self.created_at,
            'modified_at': self.modified_at
        }
    @staticmethod
    async def add(user) -> int:
        async with async_session() as session:
            user.password = user.__generate_hash(user.password)
            session.add(user)
            # Flush the session
            # This operation sends the INSERT statement to the database.
            # The database generates the primary key and returns it to SQLAlchemy,
            # which updates the 'id' attribute of the 'user' object *in memory*.
            await session.flush()
            await session.commit()
            return user.id
    @staticmethod
    async def get_user(id):
        async with async_session() as session:
            return await session.get(UserModel, id)
    @staticmethod
    async def get_user_by_email(email):
        stmt = select(UserModel).filter_by(email=email).execution_options(populate_existing=True)
        async with async_session() as session:
            return (await session.scalars(stmt)).first()
    @staticmethod
    async def isExistingUser(email):
        stmt = select(func.count()).select_from(UserModel).filter_by(email=email)
        async with async_session() as session:
            return (await session.scalar(stmt)) > 0
    @staticmethod
    async def get_users():
        stmt = select(UserModel).execution_options(populate_existing=True)
        async with async_session() as session:
            return (await session.scalars(stmt)).all()
    def __repl__(self): # return a printable representation of UserModel object, in this case we're only returning the id
        return "<id {}>".format(self.id)
class UserSchema(SQLAlchemyAutoSchema):
    """
    User Schema
    """
    class Meta:
        model = UserModel
        # Optional: include relationships, foreign keys, etc.
        include_relationships = True
        # Optional: deserialize to model instances
        load_instance = True
        # Build model instances without a Session: loading never touches the database (async-safe)
        transient = True
    id = fields.Int(dump_only=True)
    firstname = fields.Str(required=True)
    lastname = fields.Str(required=True)
    email = fields.Email(required=True)
    phone = fields.Str(required=False)
    password = fields.Str(required=True)
    lastlogin = fields.DateTime(required=False)
    created_at = fields.DateTime(dump_only=True)
    modified_at = fields.DateTime(dump_only=True)