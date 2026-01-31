from datetime import datetime
from sqlalchemy import Integer, String, DateTime, select
from marshmallow import fields, Schema
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema, auto_field
from sqlalchemy.sql import func
from typing import List
from sqlalchemy.orm import Mapped, mapped_column, relationship, Session, joinedload
from .base import Base
from .BookModel import BookModel, BookSchema
from .base import Base
from . import engine
class AuthorModel(Base):
    """
    Author Model
    https://marshmallow-sqlalchemy.readthedocs.io/en/latest/
    """
    __tablename__ = 'authors'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    firstname: Mapped[str] = mapped_column(String(128), nullable=False)
    lastname: Mapped[str] = mapped_column(String(128), nullable=False)
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False, index=True)
    phone: Mapped[str] = mapped_column(String(15), unique=True, nullable=True, index=True)
    created_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    modified_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    books: Mapped[List["BookModel"]] = relationship(backref="authors", lazy="select")
    @classmethod
    def fromdata(cls, data):
        author = AuthorModel()
        author.firstname = data.get("firstname")
        author.lastname = data.get("lastname")
        author.email = data.get("email")
        author.phone = data.get("phone")
        author.created_at = func.now()
        author.modified_at = func.now()
        return author
    def save(self):
        with Session(engine) as session:
            session.commit()
    def update(self, data):
        for key, item in data.items():
            setattr(self, key, item)
        self.modified_at = func.now()
        with Session(engine) as session:
            session.commit()
    def delete(self):
        with Session(engine) as session:
            session.delete(self)
            session.commit()
    def hasBooks(self):
        with Session(engine) as session:
            return self.books
    def bookCount(self):
        with Session(engine) as session:
            return len(list(self.books))
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
    def add(author) -> int:
        with Session(engine) as session:
            session.add(author)
            # Flush the session
            # This operation sends the INSERT statement to the database.
            # The database generates the primary key and returns it to SQLAlchemy,
            # which updates the 'id' attribute of the 'new_user' object *in memory*.
            session.flush()
            session.commit()
            return author.id       
    @staticmethod
    def get_author(id):
        # Usage and parameters are the same as that of Session.execute(); the return result is a ScalarResult filtering object which will return single elements rather than Row objects.
        with Session(engine) as session:
            return session.get(AuthorModel, id)
    @staticmethod
    def get_author_by_firstname(firstname):
        stmt = select(AuthorModel).filter_by(firstname=firstname).options(joinedload(AuthorModel.books)).execution_options(populate_existing=True)
        with Session(engine) as session:
            return session.scalars(stmt).first()
    @staticmethod
    def get_author_by_lastname(lastname):
        stmt = select(AuthorModel).filter_by(lastname=lastname).options(joinedload(AuthorModel.books)).execution_options(populate_existing=True)
        with Session(engine) as session:
            return session.scalars(stmt).first()
    @staticmethod
    def get_author_by_email(email):
        stmt = select(AuthorModel).filter_by(email=email).options(joinedload(AuthorModel.books)).execution_options(populate_existing=True)
        with Session(engine) as session:
            return session.scalars(stmt).first()
    @staticmethod
    def isExistingAuthor(email):
        with Session(engine) as session:
            return session.query(AuthorModel).filter_by(email=email).count() > 0
    @staticmethod
    def get_authors_like(name):
        stmt = select(AuthorModel).filter(AuthorModel.firstname.ilike(f"%{name}%"), AuthorModel.lastname.ilike(f"%{name}%")).options(joinedload(AuthorModel.books)).execution_options(populate_existing=True)
        with Session(engine) as session:
            return session.scalars(stmt).all()
    @staticmethod
    def get_authors():
        stmt = select(AuthorModel).execution_options(populate_existing=True)
        # Usage and parameters are the same as that of Session.execute(); the return result is a ScalarResult filtering object which will return single elements rather than Row objects.
        with Session(engine) as session:
            authors = session.scalars(stmt).all()
            for author in authors:
                author.bookcount = len(list(author.books))
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
    id = fields.Int(dump_only=True)
    firstname = fields.Str(required=True)
    lastname = fields.Str(required=True)
    email = fields.Email(required=True)
    phone = fields.Str(required=False)
    created_at = fields.DateTime(dump_only=True)
    modified_at = fields.DateTime(dump_only=True)
    books = fields.Nested(BookSchema, many=True)