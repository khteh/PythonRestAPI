from flask import request, json, Response, Blueprint, g
from models.UserModel import UserModel, UserSchema
from common.Authentication import Authentication
from common.Response import custom_response

user_api = Blueprint("users", __name__)
user_schema = UserSchema()
@user_api.route("/", methods=["POST"])
def create():
    """
    Create User
    """
    req_data = request.get_json()
    #print(f"create() request data: {req_data}")
    data, error = user_schema.load(req_data)
    if error:
        return custom_response(error, 400)
    # Check if user already exists in the database
    user = UserModel.get_user_by_email(data.get("email"))
    if user:
        message = {"error": "User already exists!"}
        return custom_response(message, 400)
    user = UserModel(data)
    user.save()
    ser_data = user_schema.dump(user).data
    #print(f"create() user id: {ser_data.get('id')}")
    token = Authentication.generate_token(ser_data.get("id"))
    #print(f"create() token: {token}")
    return custom_response({"jwt_token": token}, 201)

@user_api.route("/login", methods=["POST"])
def login():
    """
    User Login
    """
    req_data = request.get_json()
    data, error = user_schema.load(req_data, partial=True)
    if error:
        return custom_response(error, 400)
    if not data.get("email") or not data.get("password"):
        return custom_response({"error": "You need an email and password to login"}, 400)
    user = UserModel.get_user_by_email(data.get("email"))
    if not user:
        return custom_response({"error": "Invalid user!"}, 400)
    if not user.check_hash(data.get("password")):
        return custom_response({"error": "Invalid email or password!"}, 400)
    ser_data = user_schema.dump(user).data
    token = Authentication.generate_token(ser_data.get("id"))
    return custom_response({"jwt_token": token}, 200)

@user_api.route("/")
@Authentication.auth_required
def get_all():
    return custom_response(user_schema.dump(UserModel.get_users(), many=True).data, 200)

@user_api.route("/<int:id>")
@Authentication.auth_required
def get_user(id):
    """
    Get a user
    """
    user = UserModel.get_user(id)
    if not user:
        return custom_response({"error": "User not found!"}, 400)
    return custom_response(user_schema.dump(user).data, 200)

@user_api.route("/me", methods=["PUT"])
@Authentication.auth_required
def update():
    """
    Update me
    """
    req_data = request.get_json()
    data, error = user_schema.load(req_data, partial=True)
    if error:
        return custom_response(error, 400)
    user = UserModel.get_user(g.user.get("id"))
    if not user:
        raise Exception(f"User {g.user.get('id')} not found!")
    user.update(data)
    return custom_response(user_schema.dump(user).data, 200)

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
    return custom_response(user_schema.dump(user).data, 200)