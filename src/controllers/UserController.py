import re, logging
from quart import request, Blueprint, session, render_template, flash, redirect, url_for
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
async def index():
    """
    User Index page
    """
    return await render_template("users.html", title="Welcome to Python RESTful API", users=UserModel.get_users())
	
@user_api.route("/create", methods=["GET","POST"])
async def create():
    """
    Create User
    """
    if request.method == "POST":
        try:
            form = await request.form
            if not form["firstname"]:
                await flash("Please provide firstname!", "danger")
                return redirect(url_for("user.create"))
            if not form["lastname"]:
                await flash("Please provide lastname!", "danger")
                return redirect(url_for("user.create"))			   
            emailRegex = "[\w.-]+@[\w.-]+.\w+"
            if not re.match(emailRegex, form["email"]):
                await flash("Please provide an valid email address!", "danger")
                return redirect(url_for("user.create"))
            if not form["password"]:
                await flash("Please provide an valid password!", "danger")
                return redirect(url_for("user.create"))
            if not form["password1"] or form["password"] != form["password1"]:
                await flash("Password mismatch!", "danger")
                return redirect(url_for("user.create"))
            if UserModel.isExistingUser(form['email']):
                await flash(f"Trying to register an existing user {form['email']}!", "danger")
                return redirect(url_for("user.create"))							
            req_data = {
               "firstname": form["firstname"],
			   "lastname": form["lastname"],
			   "email": form["email"],
               "password": form["password"]
			}
            print(f"create() request data: {req_data}")
            data = user_schema.load(req_data)
		    # Check if user already exists in the database
            if not data:
                await flash(f"Invalid input!", "danger")
                return redirect(url_for("user.create"))
            user = UserModel.get_user_by_email(data.get("email"))
            if user:
                await flash(f"Trying to create an existing user!", "danger")
                return redirect(url_for("user.create"))
            user = UserModel(data)
            user.save()
            ser_data = user_schema.dump(user) #.data
		    #print(f"create() user id: {ser_data.get('id')}")
            token = Authentication.generate_token(ser_data.get("id"))
		    #print(f"create() token: {token}")
            await flash(f"User created successfully!", "success")
            return redirect(url_for("user.index"))
        except ValidationError as err:
            errors = err.messages
            valid_data = err.valid_data	
            print(f"create() error! {errors}")
            await flash(f"Failed to create user! {err.messages}", "danger")
            return redirect(url_for("user.create"))
    return await render_template("user_create.html", title="Welcome to Python Flask RESTful API")

@user_api.route("/all")
@Authentication.auth_required
async def get_all():
    return custom_response(user_schema.dump(UserModel.get_users(), many=True), 200)

@user_api.route("/<int:id>", methods=["GET"])
@Authentication.auth_required
async def get_user(id):
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
async def update(id):
    """
    Update me
    """
    try:
        req_data = await request.get_json()
        data = user_schema.load(req_data, partial=True)
        if not data:
            message = {"error": "Invalid input!"}
            return custom_response(message, 400)		
        user = UserModel.get_user(id)
        if not user:
            raise Exception(f"User {id} not found!")
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
async def delete(id):
    """
    Delete me
    """
    try:
        user = UserModel.get_user(id)
        if not user:
            raise Exception(f"User {id} not found!")
        user.delete()
        logging.info(f"User {id} deleted successfully!")
        print(f"User {id} deleted successfully!")
    except ValidationError as err:
        errors = err.messages
        valid_data = err.valid_data	
        print(f"create() error! {errors}")
        logging.error(f"Failed to delete user {id}! Exception: {errors}")
        return custom_response(error, 500)		
    return custom_response({"message": f"User {id} deleted successfully!"}, 204)
