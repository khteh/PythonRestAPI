import re, logging, jsonpickle
from quart import request, json, Blueprint, session, render_template, flash, redirect, url_for
from datetime import datetime, timezone
from marshmallow import ValidationError
from sqlalchemy.orm import Mapped, mapped_column, relationship, Session
from src.common.Authentication import Authentication
from src.common.ResponseHelper import Respond
from src.models.AuthorModel import AuthorModel, AuthorSchema
from src.models.BookModel import BookModel, BookSchema
from src.models import engine
book_api = Blueprint("book", __name__)
book_schema = BookSchema()
author_schema = AuthorSchema()
@book_api.context_processor
def inject_now():
    return {'now': datetime.now(timezone.utc)}

@book_api.get("/")
@book_api.get("/index")
async def index():
    """
    Book Index page
    """
    return await Respond("books.html", title="Welcome to Python RESTful API", books=BookModel.get_books())

@book_api.route("/create", methods=["GET", "POST"])
@Authentication.auth_required("book.create")
async def create():
    """
    Create Book
    """
    if request.method == "POST":	
        user = session['user']
        try:
            form = await request.form
            if "title" not in form or not form["title"]:
                await flash("Please provide title!", "danger")
                return redirect(url_for("book.create"))		
            if "isbn" not in form or not form["isbn"]:
                await flash("Please provide isbn!", "danger")
                return redirect(url_for("book.create"))						
            if "pages" not in form or not form["pages"]:
                await flash("Please provide page count!", "danger")
                return redirect(url_for("book.create"))
            if "author" not in form or not form["author"]:
                await flash("Please provide author!", "danger")
                return redirect(url_for("book.create"))
            numberRegex = r"^(\d)+$"
            if not re.match(numberRegex, form["pages"]):
                await flash("Please provide an valid page count!", "danger")
                return redirect(url_for("book.create"))
            # https://www.oreilly.com/library/view/regular-expressions-cookbook/9781449327453/ch04s13.html
            # ISBN 978-0-596-52068-7
            # ISBN-13: 978-0-596-52068-7
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
            # Validate the data against BookModel schema
            with Session(engine) as dbsession:
                data = book_schema.load(req_data, session=dbsession)
                logging.debug(f"book.create(): {data.serialized}")
            if not data:
                await flash(f"Invalid input!", "danger")
                return redirect(url_for("book.create"))
            # Validate author id
            if not AuthorModel.get_author(data.author_id):
                await flash(f"Invalid author!", "danger")
                return redirect(url_for("book.create"))
            if BookModel.isExistingBook(data.isbn):
                await flash(f"Book {data.isbn} already exists!", "danger")
                return redirect(url_for("book.create"))
            id = BookModel.add(data)
            book = BookModel.get_book(id)
            await flash(f"Book {book.title} created successfully!", "success")
            logging.info(f"User {user['email']} created book {book.title} successfully!")
            return redirect(url_for("book.index"))
        except ValidationError as err:
            errors = err.messages
            valid_data = err.valid_data	
            await flash(f"Failed to create book! {err.messages}", "danger")
            logging.exception(f"User {user['email']} failed to create book! Exception: {errors}")
            return redirect(url_for("book.create"))
    authors = author_schema.dump(AuthorModel.get_authors(), many=True)
    return await Respond("book_create.html", title="Welcome to Python Flask RESTful API", authors = authors)
	
@book_api.route("/all")
@Authentication.auth_required("book.get_all")
async def get_all():
    """
    Get All Books
    """
    return custom_response(book_schema.dump(BookModel.get_books(), many=True), 200)

@book_api.route("/author/firstname/<string:firstname>")
@Authentication.auth_required("book.get_all_by_author_firstname")
async def get_all_by_author_firstname(firstname):
    """
    Get All Books by auhor's firstname
    """
    author = author_schema.dump(AuthorModel.get_author_by_firstname(firstname))
    if not author:
        return custom_response({"error": f"Author {firstname} not found!"}, 404)
    return custom_response(book_schema.dump(author["books"], many=True), 200)

@book_api.route("/author/lastname/<string:lastname>")
@Authentication.auth_required("book.get_all_by_author_lastname")
async def get_all_by_author_lastname(lastname):
    """
    Get All Books by auhor's lastname
    """
    author = author_schema.dump(AuthorModel.get_author_by_lastname(lastname))
    if not author:
        return custom_response({"error": f"Author {lastname} not found!"}, 404)
    return custom_response(book_schema.dump(author["books"], many=True), 200)

@book_api.route("/author/email/<string:email>")
@Authentication.auth_required("book.get_all_by_author_email")
async def get_all_by_author_email(email):
    """
    Get All Books by auhor's email
    """
    author = AuthorModel.get_author_by_email(email)
    if not author:
        #return custom_response({"error": f"Author {email} not found!"}, 404)
        await flash(f"Invalid author {email}!", "danger")
        return await Respond("books.html", title="Welcome to Python RESTAPI")
    #return custom_response(book_schema.dump(author["books"], many=True), 200)
    return await Respond("books.html", title="Welcome to Python RESTAPI", books=author.books, author=author)

@book_api.route("/<int:id>")
@Authentication.auth_required("book.get_book")
async def get_book(id):
    """
    Get Book 'id'
    """
    book = book_schema.dump(BookModel.get_book(id))
    if not book:
        return custom_response({"error": f"Book {id} not found!"}, 404)
    return custom_response(book_schema.dump(book), 200)
	
@book_api.route("/isbn/<string:isbn>")
@Authentication.auth_required("book.get_book_by_isbn")
async def get_book_by_isbn(isbn):
    """
    Get Book 'isbn'
    """
    book = book_schema.dump(BookModel.get_book_by_isbn(isbn))
    if not book:
        return custom_response({"error": f"Book {id} not found!"}, 404)
    return custom_response(book_schema.dump(book), 200)
	
@book_api.route("/title/<string:title>")
@Authentication.auth_required("book.get_book_by_title")
async def get_book_by_title(title):
    """
    Get Book 'title'
    """
    book = book_schema.dump(BookModel.get_book_by_title(title))
    if not book:
        return custom_response({"error": f"Book {id} not found!"}, 404)
    return custom_response(book_schema.dump(book), 200)

@book_api.route("/<int:id>", methods=["PUT"])
@Authentication.auth_required("book.update")
async def update(id):
    """
    Update Book 'id'
    """
    try:
        user = session['user']
        req_data = await request.get_json()
        data = book_schema.load(req_data, partial=True)
        if not data:
            await flash(f"Failed to update book {id} with invalid input data!", "warning")
            return redirect(url_for("book.index"))
        book = BookModel.get_book(id)
        if not book:
            await flash(f"Trying to update non-existing book {id}!", "warning")
            return redirect(url_for("book.index"))
        book.update(data)
        logging.info(f"User {user['email']} updated book {id} successfully!")
        await flash(f"Book {book.title} updated successfully!", "success")
    except ValidationError as err:
        errors = err.messages
        valid_data = err.valid_data	
        logging.exception(f"User {user['email']} failed to update book {id}! Exception: {errors}")
        await flash(f"Failed to update book {id}! Exception: {errors}", "danger")
    return redirect(url_for("book.index"))

@book_api.route("/<int:id>", methods=["DELETE"])
@Authentication.auth_required("book.delete")
async def delete(id):
    """
    Delete Book 'id'
    """
    try:
        user = session['user']
        book = BookModel.get_book(id)
        if not book:
            await flash(f"Trying to delete non-existing book {id}!", "warning")
            return redirect(url_for("book.index"))
        book.delete()
        logging.warning(f"User {user['email']} deleted book {book.title} successfully!")
        await flash(f"Book {book.title} deleted successfully!", "success")
    except ValidationError as err:
        errors = err.messages
        valid_data = err.valid_data	
        logging.exception(f"User {user['email']} failed to delete book {id}! Exception: {errors}")
        await flash(f"Failed to delete book {id}! Exception: {errors}", "danger")
    return redirect(url_for("book.index"))