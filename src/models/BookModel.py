from datetime import datetime
from sqlalchemy import Integer, String, DateTime, ForeignKey, select
from marshmallow import fields, Schema
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema, auto_field
from sqlalchemy.sql import func
from sqlalchemy.orm import Mapped, mapped_column, Session
from quart import Quart
from .base import Base
from . import engine
class BookModel(Base):
    """
    Book Model
    https://marshmallow-sqlalchemy.readthedocs.io/en/latest/
    """
    __tablename__ = "books"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(128), nullable=False)
    isbn: Mapped[str] = mapped_column(String(255), nullable=False)
    page_count: Mapped[int] = mapped_column(Integer, nullable=False)
    author_id: Mapped[int] = mapped_column(ForeignKey("authors.id"), nullable=False)
    created_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    modified_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    @classmethod
    def fromdata(cls, data):
        book = BookModel()
        book.author_id = data.author_id
        book.title = data.title
        book.isbn = data.isbn
        book.page_count = data.page_count
        book.created_at = func.now()
        book.modified_at = func.now()
        return book
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
    @property
    def serialized(self):
        """Return object data in serializable format"""
        return {
            'id': self.id,
            'title': self.title,
            'isbn': self.isbn,
            'page_count': self.page_count,
            'author_id': self.author_id,
            'created_at': self.created_at,
            'modified_at': self.modified_at
        }
    @staticmethod
    def add(book) -> int:
        with Session(engine) as session:
            session.add(book)
            # Flush the session
            # This operation sends the INSERT statement to the database.
            # The database generates the primary key and returns it to SQLAlchemy,
            # which updates the 'id' attribute of the 'new_user' object *in memory*.
            session.flush()
            session.commit()
            return book.id
    @staticmethod
    def get_books():
        stmt = select(BookModel).execution_options(populate_existing=True)
        with Session(engine) as session:
            return session.scalars(stmt).all()
    @staticmethod
    def get_book(id):
        # Usage and parameters are the same as that of Session.execute(); the return result is a ScalarResult filtering object which will return single elements rather than Row objects.
        with Session(engine) as session:
            return session.get(BookModel, id)
    @staticmethod
    def get_book_by_isbn(isbn):
        stmt = select(BookModel).filter_by(isbn=isbn).execution_options(populate_existing=True)
        # Usage and parameters are the same as that of Session.execute(); the return result is a ScalarResult filtering object which will return single elements rather than Row objects.
        with Session(engine) as session:
            return session.scalars(stmt).first()
    @staticmethod
    def get_books_by_title(title):
        stmt = select(BookModel).filter_by(title=title).execution_options(populate_existing=True)
        # Usage and parameters are the same as that of Session.execute(); the return result is a ScalarResult filtering object which will return single elements rather than Row objects.
        with Session(engine) as session:
            return session.scalars(stmt).all()
    @staticmethod
    def isExistingBook(isbn):
        # Usage and parameters are the same as that of Session.execute(); the return result is a ScalarResult filtering object which will return single elements rather than Row objects.
        with Session(engine) as session:
            return session.query(BookModel).filter_by(isbn=isbn).count() > 0
    @staticmethod
    def get_books_like(title):
        stmt = select(BookModel.title, BookModel.isbn).where(BookModel.name.ilike(f"%{title}%"))
        with Session(engine) as session:
            return session.scalars(stmt).all()
    def __repl__(self): # return a printable representation of BookpostModel object, in this case, we're only returning the id
        return "<id {}".format(self.id)
class BookSchema(SQLAlchemyAutoSchema):
    """
    Book Schema
    """
    class Meta:
        model = BookModel
        # Optional: include relationships, foreign keys, etc.
        include_relationships = True
        # Optional: deserialize to model instances
        load_instance = True 
    id = fields.Int(dump_only=True)
    title = fields.Str(required=True)
    isbn = fields.Str(required=True)
    page_count = fields.Str(required=True)
    author_id = fields.Int(required=True)
    created_at = fields.DateTime(dump_only=True)
    modified_at = fields.DateTime(dump_only=True)