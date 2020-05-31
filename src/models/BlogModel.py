from . import db
from marshmallow import fields, Schema
import datetime

class BlogModel(db.Model):
    """
    Blog Model
    """
    __tablename__ = "blogs"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(123), nullable=False)
    contents = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime)
    modified_at = db.Column(db.DateTime)
    owner_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    def __init__(self, data):
        self.owner_id = data.get("owner_id")
        self.title = data.get("title")
        self.contents = data.get("contents")
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
    def get_blogs():
        return BlogModel.query.all()
    @staticmethod
    def get_blog(id):
        return BlogModel.query.get(id)
    def __repl__(self): # return a printable representation of BlogpostModel object, in this case, we're only returning the id
        return "<id {}".format(self.id)
class BlogSchema(Schema):
    """
    Blog Schema
    """
    id = fields.Int(dump_only=True)
    title = fields.Str(required=True)
    contents = fields.Str(required=True)
    owner_id = fields.Int(required=True)
    created_at = fields.DateTime(dump_only=True)
    modified_at = fields.DateTime(dump_only=True)