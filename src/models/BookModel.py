from datetime import datetime, timezone
from sqlalchemy import Integer, String, DateTime, ForeignKey, select, func
from marshmallow import fields, Schema
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema, auto_field
from sqlalchemy.orm import Mapped, mapped_column
from quart import Quart
from .base import Base
from . import async_session
class BookModel(Base):
    """
    Book Model
    https://marshmallow-sqlalchemy.readthedocs.io/en/latest/
    All database access is async (SQLAlchemy AsyncSession).
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
        book.created_at = datetime.now(timezone.utc)
        book.modified_at = datetime.now(timezone.utc)
        return book
    async def save(self):
        async with async_session() as session:
            session.add(self)
            await session.commit()
    async def update(self, data):
        values = data if isinstance(data, dict) else {k: v for k, v in vars(data).items() if not k.startswith("_")}
        values["modified_at"] = datetime.now(timezone.utc)
        async with async_session() as session:
            book = await session.get(BookModel, self.id)
            for key, item in values.items():
                setattr(book, key, item)
            await session.commit()
            for key, item in values.items():
                setattr(self, key, item)
    async def delete(self):
        async with async_session() as session:
            book = await session.get(BookModel, self.id)
            if book:
                await session.delete(book)
                await session.commit()
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
    async def add(book) -> int:
        async with async_session() as session:
            session.add(book)
            # Flush the session
            # This operation sends the INSERT statement to the database.
            # The database generates the primary key and returns it to SQLAlchemy,
            # which updates the 'id' attribute of the 'book' object *in memory*.
            await session.flush()
            await session.commit()
            return book.id
    @staticmethod
    async def get_books():
        stmt = select(BookModel).execution_options(populate_existing=True)
        async with async_session() as session:
            return (await session.scalars(stmt)).all()
    @staticmethod
    async def get_book(id):
        async with async_session() as session:
            return await session.get(BookModel, id)
    @staticmethod
    async def get_book_by_isbn(isbn):
        stmt = select(BookModel).filter_by(isbn=isbn).execution_options(populate_existing=True)
        async with async_session() as session:
            return (await session.scalars(stmt)).first()
    @staticmethod
    async def get_books_by_title(title):
        stmt = select(BookModel).filter_by(title=title).execution_options(populate_existing=True)
        async with async_session() as session:
            return (await session.scalars(stmt)).all()
    @staticmethod
    async def isExistingBook(isbn):
        stmt = select(func.count()).select_from(BookModel).filter_by(isbn=isbn)
        async with async_session() as session:
            return (await session.scalar(stmt)) > 0
    @staticmethod
    async def get_books_like(title):
        stmt = select(BookModel.title, BookModel.isbn).where(BookModel.title.ilike(f"%{title}%"))
        async with async_session() as session:
            return (await session.execute(stmt)).all()
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
        # Build model instances without a Session: loading never touches the database (async-safe)
        transient = True
    id = fields.Int(dump_only=True)
    title = fields.Str(required=True)
    isbn = fields.Str(required=True)
    page_count = fields.Str(required=True)
    author_id = fields.Int(required=True)
    created_at = fields.DateTime(dump_only=True)
    modified_at = fields.DateTime(dump_only=True)