from flask import request, g, Blueprint, json, Response
from marshmallow import ValidationError
from ..common.Authentication import Authentication
from ..common.Response import custom_response
from ..models.AuthorModel import AuthorModel, AuthorSchema
author_api = Blueprint("authors", __name__)
author_schema = AuthorSchema()
@author_api.route("/", methods=["POST"])
@Authentication.auth_required
def create():
    """
    Create Author
    """
    try:
        req_data = request.get_json()
        data = author_schema.load(req_data)
        if not data:
            message = {"error": "Invalid input!"}
            return custom_response(message, 400)
        author = author_schema.dump(AuthorModel.get_author_by_email(data.get("email")))
        if author:
            message = {"error": "Author already exists!"}
            return custom_response(message, 400)
        author = AuthorModel(data)
        author.save()
        return custom_response(author_schema.dump(author), 201)
    except ValidationError as err:
        errors = err.messages
        valid_data = err.valid_data	
        print(f"create() error! {errors}")		
        return custom_response(errors, 500)
		
@author_api.route("/<int:id>")
@Authentication.auth_required
def get_author(id):
    """
    Get Auhor 'id'
    """
    author = auhor_schema.dump(AuthorModel.get_author(id))
    if not author:
        return custom_response({"error": f"Author {id} not found!"}, 404)
    return custom_response(author_schema.dump(author), 200)

@author_api.route("/firstname/<string:firstname>")
@Authentication.auth_required
def get_by_firstname(firstname):
    """
    Get Author by firstname
    """
    print(f"get_author_by_author_firstname: {firstname}")
    return custom_response(author_schema.dump(AuthorModel.get_author_by_firstname(firstname)), 200)

@author_api.route("/lastname/<string:lastname>")
@Authentication.auth_required
def get_by_lastname(lastname):
    """
    Get Author by lastname
    """
    return custom_response(author_schema.dump(AuthorModel.get_author_by_firstname(lastname)), 200)

@author_api.route("/email/<string:email>")
@Authentication.auth_required
def get_by_email(email):
    """
    Get Author by email
    """
    return custom_response(author_schema.dump(AuthorModel.get_author_by_firstname(email)), 200)

@author_api.route("/")
@Authentication.auth_required
def get_all():
    """
    Get All Authors
    """
    return custom_response(author_schema.dump(AuthorModel.get_authors(), many=True), 200)

@author_api.route("/<int:id>", methods=["PUT"])
@Authentication.auth_required
def update(id):
    """
    Update Author 'id'
    """
    try:
        req_data = request.get_json()
        data = author_schema.load(req_data, partial=True)
        if not data:
            message = {"error": "Invalid input!"}
            return custom_response(message, 400)		
        author = AuthorModel.get_author(id)
        if not author:
            return custom_response({"error": f"Author {id} not found!"}, 404)
        author.update(data)
        return custom_response(author_schema.dump(author), 200)
    except ValidationError as err:
        errors = err.messages
        valid_data = err.valid_data	
        print(f"Failed to update author {id} error! {errors}")		
        return custom_response(error, 500)

@author_api.route("/<int:id>", methods=["DELETE"])
@Authentication.auth_required
def delete(id):
    """
    Delete Author 'id'
    """
    try:
        author = AuthorModel.get_author(id)
        if not author:
            return custom_response({"error": f"Author {id} not found!"}, 404)
        data = author_schema.dump(author)
        author.delete()
        print(f"Author {id} deleted successfully!")
        return custom_response({"message": f"Author {id} deleted successfully!"}, 204)
    except ValidationError as err:
        errors = err.messages
        valid_data = err.valid_data	
        print(f"Failed to delete author {id} error! {errors}")		
        return custom_response(error, 500)
