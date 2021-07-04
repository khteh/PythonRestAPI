from . import db
from marshmallow import fields, Schema
import datetime

class BookModel(db.Model):
    """
    Book Model
    """
    __tablename__ = "books"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(128), nullable=False)
    isbn = db.Column(db.String(255), nullable=False)
    page_count = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime(timezone=True))
    modified_at = db.Column(db.DateTime(timezone=True))
    author_id = db.Column(db.Integer, db.ForeignKey("authors.id"), nullable=False)
    def __init__(self, data):
        self.author_id = data.get("author_id")
        self.title = data.get("title")
        self.isbn = data.get("isbn")
        self.page_count = data.get("page_count")
        self.created_at = data.get("created_at")
        self.modified_at = data.get("modified_at")
    def save(self):
        db.session.add(self)
        db.session.commit()
    def update(self, data):
        for key, item in data.items():
            setattr(self, key, item)
        self.modified_at = datetime.datetime.utcnow
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
        return BookModel.query.with_entities(BookModel.title, BbookModel.isbn).filter(BookModel.name.ilike(f"%{title}%")).all()
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
