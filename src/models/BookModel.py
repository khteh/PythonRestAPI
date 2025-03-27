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
from .base import Base
from .Database import db

class BookModel(Base):
    """
    Book Model
    """
    __tablename__ = "books"
    id: Mapped[int] = mapped_column(sa.Identity(), primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(sa.String(128), nullable=False)
    isbn: Mapped[str] = mapped_column(sa.String(255), nullable=False)
    page_count: Mapped[int] = mapped_column(sa.Integer, nullable=False)
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
    author_id: Mapped[int] = mapped_column(sa.ForeignKey("authors.id"), nullable=False)
    def __init__(self, data):
        self.author_id = data.get("author_id")
        self.title = data.get("title")
        self.isbn = data.get("isbn")
        self.page_count = data.get("page_count")
        self.created_at = func.now()
        self.modified_at = func.now()
    def save(self):
        db.session.add(self)
        db.session.commit()
    def update(self, data):
        for key, item in data.items():
            setattr(self, key, item)
        self.modified_at = func.now()
        db.session.commit()
    def delete(self):
        db.session.delete(self)
        db.session.commit()
    @staticmethod
    def get_books():
        return BookModel.query.all()
    @staticmethod
    def get_book(id):
        return BookModel.query.get(id)
    @staticmethod
    def get_book_by_isbn(isbn):
        return BookModel.query.filter_by(isbn=isbn)
    @staticmethod
    def get_books_by_title(title):
        return BookModel.query.filter_by(title=title)
    @staticmethod
    def isExistingBook(isbn):
        return BookModel.query.filter_by(isbn = isbn).count() > 0
    @staticmethod
    def get_books_like(title):
        return BookModel.query.with_entities(BookModel.title, BookModel.isbn).filter(BookModel.name.ilike(f"%{title}%")).all()
    def __repl__(self): # return a printable representation of BookpostModel object, in this case, we're only returning the id
        return "<id {}".format(self.id)
class BookSchema(Schema):
    """
    Book Schema
    """
    id = fields.Int(dump_only=True)
    title = fields.Str(required=True)
    isbn = fields.Str(required=True)
    page_count = fields.Str(required=True)
    author_id = fields.Int(required=True)
    created_at = fields.DateTime(dump_only=True)
    modified_at = fields.DateTime(dump_only=True)
