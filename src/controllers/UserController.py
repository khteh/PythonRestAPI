from flask import request, json, Response, Blueprint, g, render_template, flash
from marshmallow import ValidationError
from datetime import datetime
from ..models.UserModel import UserModel, UserSchema
from ..common.Authentication import Authentication
from ..common.Response import custom_response
user_api = Blueprint("users", __name__)
user_schema = UserSchema()
@user_api.context_processor
def inject_now():
    return {'now': datetime.utcnow()}

@user_api.route("/", methods=["POST"])
def create():
    """
    Create User
    """
    try:
        req_data = request.get_json()
        print(f"create() request data: {req_data}")
        data = user_schema.load(req_data)
		# Check if user already exists in the database
        if not data:
            message = {"error": "Invalid input!"}
            return custom_response(message, 400)
        user = UserModel.get_user_by_email(data.get("email"))
        if user:
            message = {"error": "User already exists!"}
            return custom_response(message, 400)
        user = UserModel(data)
        user.save()
        ser_data = user_schema.dump(user) #.data
		#print(f"create() user id: {ser_data.get('id')}")
        token = Authentication.generate_token(ser_data.get("id"))
		#print(f"create() token: {token}")
        return custom_response({"jwt_token": token}, 201)
    except ValidationError as err:
        errors = err.messages
        valid_data = err.valid_data	
        print(f"create() error! {errors}")		
        return custom_response(error, 500)

@user_api.route("/")
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

@user_api.route("/me", methods=["PUT"])
@Authentication.auth_required
def update():
    """
    Update me
    """
    try:
        req_data = request.get_json()
        data = user_schema.load(req_data, partial=True)
        if not data:
            message = {"error": "Invalid input!"}
            return custom_response(message, 400)		
        user = UserModel.get_user(g.user.get("id"))
        if not user:
            raise Exception(f"User {g.user.get('id')} not found!")
        user.update(data)
        return custom_response(user_schema.dump(user), 200)
    except ValidationError as err:
        errors = err.messages
        valid_data = err.valid_data	
        print(f"create() error! {errors}")		
        return custom_response(error, 500)

@user_api.route("/me", methods=["DELETE"])
@Authentication.auth_required
def delete():
    """
    Delete me
    """
    user = UserModel.get_user(g.user.get("id"))
    if not user:
        raise Exception(f"User {g.user.get('id')} not found!")
    user.delete()
    print(f"User {g.user.get('id')} deleted successfully!")
    return custom_response({"message": f"User {g.user.get('id')} deleted successfully!"}, 204)

@user_api.route("/me")
@Authentication.auth_required
def me():
    """
    Get me
    """
    user = UserModel.get_user(g.user.get("id"))
    if not user:
        raise Exception(f"User {g.user.get('id')} not found!")
    return custom_response(user_schema.dump(user), 200)