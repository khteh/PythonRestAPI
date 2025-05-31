import re, logging, jsonpickle
from quart import request, Blueprint, session, render_template, flash, redirect, url_for
from marshmallow import ValidationError
from datetime import datetime, timezone
from src.common.Response import custom_response
from src.common.Authentication import Authentication
from src.common.ResponseHelper import Respond
from src.models.AuthorModel import AuthorModel, AuthorSchema
author_api = Blueprint("author", __name__)
author_schema = AuthorSchema()
@author_api.context_processor
def inject_now():
    return {'now': datetime.now(timezone.utc)}

@author_api.get("/")
@author_api.get("/index")
async def index():
    """
    Author Index page
    """
    authors = AuthorModel.get_authors()
    for author in authors:
        author.bookcount = author.bookCount()
    return await Respond("authors.html", title="Welcome to Python RESTful API", authors=authors)

@author_api.route("/create", methods=["GET", "POST"])
@Authentication.auth_required("author.create")
async def create():
    """
    Create Author
    """
    if request.method == "POST":	
        user = session['user']
        logging.debug(f"author.create user: {user}")
        try:
            form = await request.form
            if "firstname" not in form or not form["firstname"]:
                await flash("Please provide firstname!", "danger")
                return redirect(url_for("author.create"))
            if "lastname" not in form or not form["lastname"]:
                await flash("Please provide lastname!", "danger")
                return redirect(url_for("author.create"))			   
            emailRegex = r"[\w.-]+@[\w.-]+.\w+"
            if "email" not in form or not re.match(emailRegex, form["email"]):
                await flash("Please provide an valid email address!", "danger")
                return redirect(url_for("author.create"))		
            phoneRegex = r"^(\+\d{1,3}\-?)*(\d{8,10})$"
            if "phone" not in form or not re.match(phoneRegex, form["phone"]):
                await flash("Please provide an valid phone number!", "danger")
                return redirect(url_for("author.create"))
            if AuthorModel.isExistingAuthor(form['email']):
                await flash(f"Trying to add an existing author {form['email']}!", "danger")
                return redirect(url_for("author.create"))			
            req_data = {
               "firstname": form["firstname"],
			   "lastname": form["lastname"],
			   "email": form["email"],
			   "phone": form["phone"],
			}
            logging.debug(f"author.create() request data: {req_data}")
            data = author_schema.load(req_data)
            if not data:
                await flash(f"Invalid input!", "danger")
                return redirect(url_for("author.create"))
            author = author_schema.dump(AuthorModel.get_author_by_email(data.get("email")))
            if author:
                await flash(f"Trying to create an existing author!", "danger")
                return redirect(url_for("author.create"))
            author = AuthorModel(data)
            author.save()
            await flash(f"Author {author.firstname}, {author.lastname} created successfully!", "success")
            logging.info(f"User {user['email']} created author {author.email} successfully!")
            return redirect(url_for("author.index"))
        except ValidationError as err:
            errors = err.messages
            valid_data = err.valid_data	
            logging.exception(f"User {user['email']} failed to creat author! Exception: {errors}")
            await flash(f"Failed to create author! {err.messages}", "danger")
            return redirect(url_for("author.create"))
    return await Respond("author_create.html", title="Welcome to Python Flask RESTful API")
		
@author_api.route("/<int:id>")
@Authentication.auth_required("author.get_author")
async def get_author(id):
    """
    Get Auhor 'id'
    """
    author = author_schema.dump(AuthorModel.get_author(id))
    if not author:
        return custom_response({"error": f"Author {id} not found!"}, 404)
    return custom_response(author_schema.dump(author), 200)

@author_api.route("/firstname/<string:firstname>")
@Authentication.auth_required("author.get_by_firstname")
async def get_by_firstname(firstname):
    """
    Get Author by firstname
    """
    logging.debug(f"get_author_by_author_firstname: {firstname}")
    return custom_response(author_schema.dump(AuthorModel.get_author_by_firstname(firstname)), 200)

@author_api.route("/lastname/<string:lastname>")
@Authentication.auth_required("author.get_by_lastname")
async def get_by_lastname(lastname):
    """
    Get Author by lastname
    """
    return custom_response(author_schema.dump(AuthorModel.get_author_by_firstname(lastname)), 200)

@author_api.route("/email/<string:email>")
@Authentication.auth_required("author.get_by_email")
async def get_by_email(email):
    """
    Get Author by email
    """
    return custom_response(author_schema.dump(AuthorModel.get_author_by_firstname(email)), 200)

@author_api.route("/all")
@Authentication.auth_required("author.get_all")
async def get_all():
    """
    Get All Authors
    """
    return custom_response(author_schema.dump(AuthorModel.get_authors(), many=True), 200)

@author_api.route("/update/<int:id>", methods=["PUT"])
@Authentication.auth_required("author.update")
async def update(id):
    """
    Update Author 'id'
    """
    try:
        user = session['user']
        req_data = await request.get_json()
        data = author_schema.load(req_data, partial=True)
        if not data:
            await flash(f"Failed to update author {id} with invalid input data!", "warning")
            return redirect(url_for("author.index"))
        author = AuthorModel.get_author(id)
        if not author:
            await flash(f"Trying to update non-existing author {id}!", "warning")
            return redirect(url_for("author.index"))
        author.update(data)
        logging.info(f"User {user['email']} updated author {author.email} successfully!")
        await flash(f"Author {author.firstname}, {author.lastname} updated successfully!", "success")
    except ValidationError as err:
        errors = err.messages
        valid_data = err.valid_data
        logging.exception(f"User {user['email']} failed to update author {id}! Exception: {errors}")
        await flash(f"Failed to update author {id}! Exception: {errors}", "danger")
    return redirect(url_for("author.index"))

@author_api.route("/delete/<int:id>", methods=["DELETE"])
@Authentication.auth_required("author.delete")
async def delete(id):
    """
    Delete Author 'id'
    """
    try:
        user = session['user']
        author = AuthorModel.get_author(id)
        if not author:
            await flash(f"Trying to delete non-existing author {id}!", "warning")
            return redirect(url_for("author.index"))
        author.delete()
        logging.warning(f"User {user['email']} deleted author {author.email} successfully!")
        await flash(f"Author {author.firstname}, {author.lastname} deleted successfully!", "success")
    except ValidationError as err:
        errors = err.messages
        valid_data = err.valid_data	
        logging.exception(f"User {user['email']} failed to delete author {id}! Exception: {errors}")
        await flash(f"Failed to delete author {id}! Exception: {errors}", "danger")
    return redirect(url_for("user.index"))