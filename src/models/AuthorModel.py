from datetime import datetime, timezone
from sqlalchemy import Integer, String, DateTime, select, func
from marshmallow import fields, Schema
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema, auto_field
from typing import List
from sqlalchemy.orm import Mapped, mapped_column, relationship, backref, joinedload
from .base import Base
from .BookModel import BookModel, BookSchema
from . import async_session
class AuthorModel(Base):
    """
    Author Model
    https://marshmallow-sqlalchemy.readthedocs.io/en/latest/
    All database access is async (SQLAlchemy AsyncSession). Lazy loading is not possible with AsyncSession,
    therefore relationships are eager loaded (lazy="selectin") or loaded explicitly with joinedload().
    """
    __tablename__ = 'authors'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    firstname: Mapped[str] = mapped_column(String(128), nullable=False)
    lastname: Mapped[str] = mapped_column(String(128), nullable=False)
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False, index=True)
    phone: Mapped[str] = mapped_column(String(15), unique=True, nullable=True, index=True)
    created_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    modified_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    books: Mapped[List["BookModel"]] = relationship(backref=backref("authors", lazy="selectin"), lazy="selectin")
    @classmethod
    def fromdata(cls, data):
        author = AuthorModel()
        author.firstname = data.get("firstname")
        author.lastname = data.get("lastname")
        author.email = data.get("email")
        author.phone = data.get("phone")
        author.created_at = datetime.now(timezone.utc)
        author.modified_at = datetime.now(timezone.utc)
        return author
    async def save(self):
        async with async_session() as session:
            session.add(self)
            await session.commit()
    async def update(self, data):
        values = data if isinstance(data, dict) else {k: v for k, v in vars(data).items() if not k.startswith("_")}
        values["modified_at"] = datetime.now(timezone.utc)
        async with async_session() as session:
            author = await session.get(AuthorModel, self.id)
            for key, item in values.items():
                setattr(author, key, item)
            await session.commit()
            for key, item in values.items():
                setattr(self, key, item)
    async def delete(self):
        async with async_session() as session:
            author = await session.get(AuthorModel, self.id)
            if author:
                await session.delete(author)
                await session.commit()
    async def hasBooks(self):
        return len(self.books) > 0
    async def bookCount(self):
        return len(self.books)
    @property
    def serialized(self):
        """Return object data in serializable format"""
        return {
            'id': self.id,
            'firstname': self.firstname,
            'lastname': self.lastname,
            'email': self.email,
            'phone': self.phone,
            'books': self.books,
            'created_at': self.created_at,
            'modified_at': self.modified_at
        }
    @staticmethod
    async def add(author) -> int:
        async with async_session() as session:
            session.add(author)
            # Flush the session
            # This operation sends the INSERT statement to the database.
            # The database generates the primary key and returns it to SQLAlchemy,
            # which updates the 'id' attribute of the 'author' object *in memory*.
            await session.flush()
            await session.commit()
            return author.id
    @staticmethod
    async def get_author(id):
        async with async_session() as session:
            return await session.get(AuthorModel, id)
    @staticmethod
    async def get_author_by_firstname(firstname):
        stmt = select(AuthorModel).filter_by(firstname=firstname).options(joinedload(AuthorModel.books)).execution_options(populate_existing=True)
        async with async_session() as session:
            return (await session.scalars(stmt)).unique().first()
    @staticmethod
    async def get_author_by_lastname(lastname):
        stmt = select(AuthorModel).filter_by(lastname=lastname).options(joinedload(AuthorModel.books)).execution_options(populate_existing=True)
        async with async_session() as session:
            return (await session.scalars(stmt)).unique().first()
    @staticmethod
    async def get_author_by_email(email):
        stmt = select(AuthorModel).filter_by(email=email).options(joinedload(AuthorModel.books)).execution_options(populate_existing=True)
        async with async_session() as session:
            return (await session.scalars(stmt)).unique().first()
    @staticmethod
    async def isExistingAuthor(email):
        stmt = select(func.count()).select_from(AuthorModel).filter_by(email=email)
        async with async_session() as session:
            return (await session.scalar(stmt)) > 0
    @staticmethod
    async def get_authors_like(name):
        stmt = select(AuthorModel).filter(AuthorModel.firstname.ilike(f"%{name}%"), AuthorModel.lastname.ilike(f"%{name}%")).options(joinedload(AuthorModel.books)).execution_options(populate_existing=True)
        async with async_session() as session:
            return (await session.scalars(stmt)).unique().all()
    @staticmethod
    async def get_authors():
        stmt = select(AuthorModel).execution_options(populate_existing=True)
        async with async_session() as session:
            authors = (await session.scalars(stmt)).all()
            for author in authors:
                author.bookcount = len(author.books)
            return authors
    def __repl__(self): # return a printable representation of AuthorModel object, in this case we're only returning the id
        return "<id {}>".format(self.id)
class AuthorSchema(SQLAlchemyAutoSchema):
    """
    Author Schema
    """
    class Meta:
        model = AuthorModel
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
    created_at = fields.DateTime(dump_only=True)
    modified_at = fields.DateTime(dump_only=True)
    books = fields.Nested(BookSchema, many=True)