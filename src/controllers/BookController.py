import re, logging
from quart import request, json, Response, Blueprint, g, render_template, flash, redirect, url_for
from datetime import datetime
from marshmallow import ValidationError
from ..common.Authentication import Authentication
from ..common.Response import custom_response
from ..models.AuthorModel import AuthorModel, AuthorSchema
from ..models.BookModel import BookModel, BookSchema

book_api = Blueprint("book", __name__)
book_schema = BookSchema()
author_schema = AuthorSchema()
@book_api.context_processor
def inject_now():
    return {'now': datetime.utcnow()}

@book_api.route("/index", methods=["GET"])
async def index():
    """
    Book Index page
    """
    return await render_template("books.html", title="Welcome to Python Flask RESTful API")

@book_api.route("/create", methods=["GET", "POST"])
@Authentication.auth_required
async def create():
    """
    Create Book
    """
    if request.method == "POST":	
        try:
            form = await request.form
            if not form["title"]:
                await flash("Please provide title!", "danger")
                return redirect(url_for("book.create"))		
            if not form["isbn"]:
                await flash("Please provide isbn!", "danger")
                return redirect(url_for("book.create"))						
            if not form["pages"]:
                await flash("Please provide page count!", "danger")
                return redirect(url_for("book.create"))
            if not form["author"] or (form["author"] == "Choose..."):
                await flash("Please provide author!", "danger")
                return redirect(url_for("book.create"))
            numberRegex = "^(\d)+$"
            if not re.match(numberRegex, form["pages"]):
                await flash("Please provide an valid page count!", "danger")
                return redirect(url_for("book.create"))
            # https://www.oreilly.com/library/view/regular-expressions-cookbook/9781449327453/ch04s13.html
            isbnRegex = "^(?=[0-9X]{10}$|(?=(?:[0-9]+[-●]){3})[-●0-9X]{13}$|97[89][0-9]{10}$|(?=(?:[0-9]+[-●]){4})[-●0-9]{17}$)(?:97[89][-●]?)?[0-9]{1,5}[-●]?[0-9]+[-●]?[0-9]+[-●]?[0-9X]$"
            if not re.match(isbnRegex, form["isbn"]):
                await flash("Please provide an valid ISBN!", "danger")
                return redirect(url_for("book.create"))
            if BookModel.isExistingBook(form["isbn"]):
                await flash(f"Trying to add an existing book {form['isbn']}!", "danger")
                return redirect(url_for("book.create"))				
            req_data = {
               "isbn": form["isbn"],
			   "title": form["title"],
			   "author_id": form["author"],
			   "page_count": form["pages"],
			}
            data = book_schema.load(req_data)
            if not data:
                await flash(f"Invalid input!", "danger")
                return redirect(url_for("book.create"))
            book = book_schema.dump(BookModel.get_book_by_isbn(data.get("isbn")))
            if book:
                isbn = book["isbn"]
                await flash(f"Book {isbn} already exists!", "danger")
                return redirect(url_for("book.create"))
            author_id = data["author_id"]
            author = author_schema.dump(AuthorModel.get_author(author_id))
            if not author:
                await flash(f"Invalid author!", "danger")
                return redirect(url_for("book.create"))
            print(f"book.create(): {json.dumps(data)}")			
            book = BookModel(data)
            book.save()
            await flash(f"Book created successfully!", "success")
            logging.info(f"User {g.user['id']} created a book successfully!")
            return redirect(url_for("book.index"))
        except ValidationError as err:
            errors = err.messages
            valid_data = err.valid_data	
            print(f"create() error! {errors}")		
            await flash(f"Failed to create book! {err.messages}", "danger")
            logging.error(f"User {g.user['id']} failed to create a book! Exception: {errors}")
            return redirect(url_for("book.create"))
    authors = author_schema.dump(AuthorModel.get_authors(), many=True)
    print(f"{len(authors)}")# authors: {json.dumps(authors)}")
    return await render_template("book_create.html", title="Welcome to Python Flask RESTful API", authors = authors)
	
@book_api.route("/all")
@Authentication.auth_required
async def get_all():
    """
    Get All Books
    """
    return custom_response(book_schema.dump(BookModel.get_books(), many=True), 200)

@book_api.route("/author/firstname/<string:firstname>")
@Authentication.auth_required
async def get_all_by_author_firstname(firstname):
    """
    Get All Books by auhor's firstname
    """
    author = author_schema.dump(AuthorModel.get_author_by_firstname(firstname))
    if not author:
        return custom_response({"error": f"Author {firstname} not found!"}, 404)
    return custom_response(book_schema.dump(author["books"], many=True), 200)

@book_api.route("/author/lastname/<string:lastname>")
@Authentication.auth_required
async def get_all_by_author_lastname(lastname):
    """
    Get All Books by auhor's lastname
    """
    author = author_schema.dump(AuthorModel.get_author_by_lastname(lastname))
    if not author:
        return custom_response({"error": f"Author {lastname} not found!"}, 404)
    return custom_response(book_schema.dump(author["books"], many=True), 200)

@book_api.route("/author/email/<string:email>")
@Authentication.auth_required
async def get_all_by_author_email(email):
    """
    Get All Books by auhor's email
    """
    author = author_schema.dump(AuthorModel.get_author_by_email(email))
    if not author:
        return custom_response({"error": f"Author {email} not found!"}, 404)
    return custom_response(book_schema.dump(author["books"], many=True), 200)

@book_api.route("/<int:id>")
@Authentication.auth_required
async def get_book(id):
    """
    Get Book 'id'
    """
    book = book_schema.dump(BookModel.get_book(id))
    if not book:
        return custom_response({"error": f"Book {id} not found!"}, 404)
    return custom_response(book_schema.dump(book), 200)
	
@book_api.route("/isbn/<string:isbn>")
@Authentication.auth_required
async def get_book_by_isbn(isbn):
    """
    Get Book 'isbn'
    """
    book = book_schema.dump(BookModel.get_book_by_isbn(isbn))
    if not book:
        return custom_response({"error": f"Book {id} not found!"}, 404)
    return custom_response(book_schema.dump(book), 200)
	
@book_api.route("/title/<string:title>")
@Authentication.auth_required
async def get_book_by_title(title):
    """
    Get Book 'title'
    """
    book = book_schema.dump(BookModel.get_book_by_title(title))
    if not book:
        return custom_response({"error": f"Book {id} not found!"}, 404)
    return custom_response(book_schema.dump(book), 200)

@book_api.route("/<int:id>", methods=["PUT"])
@Authentication.auth_required
async def update(id):
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
        logging.info(f"User {g.user['id']} updated book {id} successfully!")
        return custom_response(book_schema.dump(book), 200)
    except ValidationError as err:
        errors = err.messages
        valid_data = err.valid_data	
        print(f"Failed to update book {id} error! {errors}")		
        logging.error(f"User {g.user['id']} failed to update book {id}! Exception: {errors}")
        return custom_response(error, 500)

@book_api.route("/<int:id>", methods=["DELETE"])
@Authentication.auth_required
async def delete(id):
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
        logging.warning(f"User {g.user['id']} deleted book {id} successfully!")
        return custom_response({"message": f"Book {id} deleted successfully!"}, 204)
    except ValidationError as err:
        errors = err.messages
        valid_data = err.valid_data	
        print(f"Failed to delete book {id} error! {errors}")		
        logging.error(f"User {g.user['id']} failed to delete book {id}! Exception: {errors}")
        return custom_response(error, 500)
