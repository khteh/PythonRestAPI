import re, logging
from flask import request, json, Response, Blueprint, g, render_template, flash, redirect, url_for
from marshmallow import ValidationError
from datetime import datetime
from ..models.UserModel import UserModel, UserSchema
from ..common.Authentication import Authentication
from ..common.Response import custom_response
user_api = Blueprint("user", __name__)
user_schema = UserSchema()
@user_api.context_processor
def inject_now():
    return {'now': datetime.utcnow()}

@user_api.route("/index", methods=["GET"])
def index():
    """
    User Index page
    """
    return render_template("users.html", title="Welcom to Python Flask RESTful API")
	
@user_api.route("/create", methods=["GET","POST"])
def create():
    """
    Create User
    """
    if request.method == "POST":
        try:
            if not request.form["firstname"]:
                flash("Please provide firstname!", "danger")
                return redirect(url_for("user.create"))
            if not request.form["lastname"]:
                flash("Please provide lastname!", "danger")
                return redirect(url_for("user.create"))			   
            emailRegex = "[\w.-]+@[\w.-]+.\w+"
            if not re.match(emailRegex, request.form["email"]):
                flash("Please provide an valid email address!", "danger")
                return redirect(url_for("user.create"))
            if not request.form["password"]:
                flash("Please provide an valid password!", "danger")
                return redirect(url_for("user.create"))
            if not request.form["password1"] or request.form["password"] != request.form["password1"]:
                flash("Password mismatch!", "danger")
                return redirect(url_for("user.create"))
            req_data = {
               "firstname": request.form["firstname"],
			   "lastname": request.form["lastname"],
			   "email": request.form["email"],
               "password": request.form["password"]
			}
            print(f"create() request data: {req_data}")
            data = user_schema.load(req_data)
		    # Check if user already exists in the database
            if not data:
                flash(f"Invalid input!", "danger")
                return redirect(url_for("user.create"))
            user = UserModel.get_user_by_email(data.get("email"))
            if user:
                flash(f"Trying to create an existing user!", "danger")
                return redirect(url_for("user.create"))
            user = UserModel(data)
            user.save()
            ser_data = user_schema.dump(user) #.data
		    #print(f"create() user id: {ser_data.get('id')}")
            token = Authentication.generate_token(ser_data.get("id"))
		    #print(f"create() token: {token}")
            flash(f"User created successfully!", "success")
            return redirect(url_for("user.index"))
        except ValidationError as err:
            errors = err.messages
            valid_data = err.valid_data	
            print(f"create() error! {errors}")
            flash(f"Failed to create user! {err.messages}", "danger")
            return redirect(url_for("user.create"))
    return render_template("user_create.html", title="Welcom to Python Flask RESTful API")

@user_api.route("/all")
@Authentication.auth_required
def get_all():
    return custom_response(user_schema.dump(UserModel.get_users(), many=True), 200)

@user_api.route("/<int:id>", methods=["GET"])
@Authentication.auth_required
def get_user(id):
    """
    Get a user
    """
    user = UserModel.get_user(id)
    if not user:
        print(f"User id: {id} not found!")
        return custom_response({"error": f"User {id} not found!"}, 400)
    return custom_response(user_schema.dump(user), 200)

@user_api.route("/update/<int:id>", methods=["PUT"])
@Authentication.auth_required
def update(id):
    """
    Update me
    """
    try:
        req_data = request.get_json()
        data = user_schema.load(req_data, partial=True)
        if not data:
            message = {"error": "Invalid input!"}
            return custom_response(message, 400)		
        user = UserModel.get_user(g.user['id'])
        if not user:
            raise Exception(f"User {g.user.get('id')} not found!")
        user.update(data)
        logging.info(f"User {id} updated successfully!")
        return custom_response(user_schema.dump(user), 200)
    except ValidationError as err:
        errors = err.messages
        valid_data = err.valid_data	
        print(f"create() error! {errors}")
        logging.error(f"Failed to update user {id}! Exception: {errors}")
        return custom_response(error, 500)

@user_api.route("/delete/<int:id>", methods=["DELETE"])
@Authentication.auth_required
def delete(id):
    """
    Delete me
    """
    try:
        user = UserModel.get_user(g.user['id'])
        if not user:
            raise Exception(f"User {g.user.get('id')} not found!")
        user.delete()
        logging.info(f"User {id} deleted successfully!")
        print(f"User {g.user.get('id')} deleted successfully!")
    except ValidationError as err:
        errors = err.messages
        valid_data = err.valid_data	
        print(f"create() error! {errors}")
        logging.error(f"Failed to delete user {id}! Exception: {errors}")
        return custom_response(error, 500)		
    return custom_response({"message": f"User {g.user.get('id')} deleted successfully!"}, 204)