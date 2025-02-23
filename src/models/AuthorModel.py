from marshmallow import fields, Schema
from sqlalchemy.sql import func
from .BookModel import BookSchema
from datetime import datetime, timezone
from . import db, bcrypt

class AuthorModel(db.Model):
    """
    Author Model
    """
    __tablename__ = 'authors'
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(128), nullable=False)
    lastname = db.Column(db.String(128), nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False, index=True)
    phone = db.Column(db.String(15), unique=True, nullable=True, index=True)
    created_at = db.Column(db.DateTime(timezone=True))
    modified_at = db.Column(db.DateTime(timezone=True))
    books = db.relationship("BookModel", backref="authors", lazy=True)	
    # Class constructor
    def __init__(self, data):
        """
        Class Constructor
        """
        self.firstname = data.get("firstname")
        self.lastname = data.get("lastname")
        self.email = data.get("email")
        self.phone = data.get("phone")
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
    def hasBooks(self):
        return self.books
    def bookCount(self):
        return len(list(self.books))
    @staticmethod
    def get_author(id):
        return AuthorModel.query.get(id)
    @staticmethod
    def get_author_by_firstname(firstname):
        return AuthorModel.query.filter_by(firstname=firstname).first()		
    @staticmethod
    def get_author_by_lastname(lastname):
        return AuthorModel.query.filter_by(lastname=lastname).first()
    @staticmethod
    def get_author_by_email(email):
        return AuthorModel.query.filter_by(email=email).first()
    @staticmethod
    def isExistingAuthor(email):
        return AuthorModel.query.filter_by(email = email).count() > 0
    @staticmethod
    def get_authors_like(name):
        return AuthorModel.query.filter(AuthorModel.firstname.ilike(f"%{name}%"), AuthorModel.lastname.ilike(f"%{name}%")).all()
    @staticmethod
    def get_authors():
        return AuthorModel.query.all()
    def __repl__(self): # return a printable representation of AuthorModel object, in this case we're only returning the id
        return "<id {}>".format(self.id)
class AuthorSchema(Schema):
    """
    Author Schema
    """
    id = fields.Int(dump_only=True)
    firstname = fields.Str(required=True)
    lastname = fields.Str(required=True)
    email = fields.Email(required=True)
    phone = fields.Str(required=False)
    created_at = fields.DateTime(dump_only=True)
    modified_at = fields.DateTime(dump_only=True)
    books = fields.Nested(BookSchema, many=True)	