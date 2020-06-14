from flask import request, g, Blueprint, json, Response
from marshmallow import ValidationError
from ..common.Authentication import Authentication
from ..common.Response import custom_response
from ..models.BookModel import BookModel, BookSchema
from ..models.AuthorModel import AuthorModel, AuthorSchema
book_api = Blueprint("books", __name__)
book_schema = BookSchema()
author_schema = AuthorSchema()
@book_api.route("/", methods=["POST"])
@Authentication.auth_required
def create():
    """
    Create Book
    """
    try:
        req_data = request.get_json()
        data = book_schema.load(req_data)
        if not data:
            message = {"error": "Invalid input!"}
            return custom_response(message, 400)
        book = book_schema.dump(BookModel.get_book_by_isbn(data.get("isbn")))
        if book:
            isbn = book["isbn"]
            message = {"error": f"Book {isbn} already exists!"}
            return custom_response(message, 400)
        author_id = data["author_id"]
        author = author_schema.dump(AuthorModel.get_author(author_id))
        if not author:
            return custom_response({"error": f"Invalid author! {author_id}"}, 404)
        book = BookModel(data)
        book.save()
        return custom_response(book_schema.dump(book), 201)
    except ValidationError as err:
        errors = err.messages
        valid_data = err.valid_data	
        print(f"create() error! {errors}")		
        return custom_response(error, 500)

@book_api.route("/")
@Authentication.auth_required
def get_all():
    """
    Get All Books
    """
    return custom_response(book_schema.dump(BookModel.get_books(), many=True), 200)

@book_api.route("/author/firstname/<string:firstname>")
@Authentication.auth_required
def get_all_by_author_firstname(firstname):
    """
    Get All Books by auhor's firstname
    """
    author = author_schema.dump(AuthorModel.get_author_by_firstname(firstname))
    if not author:
        return custom_response({"error": f"Author {firstname} not found!"}, 404)
    return custom_response(book_schema.dump(author["books"], many=True), 200)

@book_api.route("/author/lastname/<string:lastname>")
@Authentication.auth_required
def get_all_by_author_lastname(lastname):
    """
    Get All Books by auhor's lastname
    """
    author = author_schema.dump(AuthorModel.get_author_by_lastname(lastname))
    if not author:
        return custom_response({"error": f"Author {lastname} not found!"}, 404)
    return custom_response(book_schema.dump(author["books"], many=True), 200)

@book_api.route("/author/email/<string:email>")
@Authentication.auth_required
def get_all_by_author_email(email):
    """
    Get All Books by auhor's email
    """
    author = author_schema.dump(AuthorModel.get_author_by_email(email))
    if not author:
        return custom_response({"error": f"Author {email} not found!"}, 404)
    return custom_response(book_schema.dump(author["books"], many=True), 200)

@book_api.route("/<int:id>")
@Authentication.auth_required
def get_book(id):
    """
    Get Book 'id'
    """
    book = book_schema.dump(BookModel.get_book(id))
    if not book:
        return custom_response({"error": f"Book {id} not found!"}, 404)
    return custom_response(book_schema.dump(book), 200)
	
@book_api.route("/<string:isbn>")
@Authentication.auth_required
def get_book_by_isbn(isbn):
    """
    Get Book 'isbn'
    """
    book = book_schema.dump(BookModel.get_book_by_isbn(isbn))
    if not book:
        return custom_response({"error": f"Book {id} not found!"}, 404)
    return custom_response(book_schema.dump(book), 200)
	
@book_api.route("/<string:title>")
@Authentication.auth_required
def get_book_by_title(title):
    """
    Get Book 'title'
    """
    book = book_schema.dump(BookModel.get_book_by_title(title))
    if not book:
        return custom_response({"error": f"Book {id} not found!"}, 404)
    return custom_response(book_schema.dump(book), 200)

@book_api.route("/<int:id>", methods=["PUT"])
@Authentication.auth_required
def update(id):
    """
    Update Book 'id'
    """
    try:
        req_data = request.get_json()
        data = book_schema.load(req_data, partial=True)
        if not data:
            message = {"error": "Invalid input!"}
            return custom_response(message, 400)		
        book = BookModel.get_book(id)
        if not book:
            return custom_response({"error": f"Book {id} not found!"}, 404)
        book.update(data)
        return custom_response(book_schema.dump(book), 200)
    except ValidationError as err:
        errors = err.messages
        valid_data = err.valid_data	
        print(f"Failed to update book {id} error! {errors}")		
        return custom_response(error, 500)

@book_api.route("/<int:id>", methods=["DELETE"])
@Authentication.auth_required
def delete(id):
    """
    Delete Book 'id'
    """
    try:
        book = BookModel.get_book(id)
        if not book:
            return custom_response({"error": f"Book {id} not found!"}, 404)
        data = book_schema.dump(book)
        book.delete()
        print(f"Book {id} deleted successfully!")
        return custom_response({"message": f"Book {id} deleted successfully!"}, 204)
    except ValidationError as err:
        errors = err.messages
        valid_data = err.valid_data	
        print(f"Failed to delete book {id} error! {errors}")		
        return custom_response(error, 500)
