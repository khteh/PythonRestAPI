from flask import request, json, Response, Blueprint, g, render_template, flash
from marshmallow import ValidationError
from datetime import datetime
from ..models.UserModel import UserModel, UserSchema
from ..common.Authentication import Authentication
from ..common.Response import custom_response
auth_api = Blueprint("auth", __name__)
user_schema = UserSchema()
@auth_api.context_processor
def inject_now():
    return {'now': datetime.utcnow()}

@auth_api.route("/login", methods=["GET", "POST"])
def login():
    """
    User Login
    """
    if request.method == "POST":
        try:
            req_data = {"email": request.form["username"], "password": request.form["password"]}
            data = user_schema.load(req_data, partial=True)
            if not data:
                message = {"error": "Invalid input!"}
                return render_template("login.html", title="Welcom to Python Flask RESTful API", error="Invalid input!")
                #return custom_response(message, 400)
            if not data.get("email") or not data.get("password"):
                #return custom_response({"error": "You need an email and password to login"}, 400)
                return render_template("login.html", title="Welcom to Python Flask RESTful API", error="You need an email and password to login")
            user = UserModel.get_user_by_email(data.get("email"))
            if not user:
                #return custom_response({"error": "Invalid user!"}, 400)
                return render_template("login.html", title="Welcom to Python Flask RESTful API", error="Invalid user!")
            if not user.check_hash(data.get("password")):
                #return custom_response({"error": "Invalid email or password!"}, 400)
                return render_template("login.html", title="Welcom to Python Flask RESTful API", error="Invalid email or password!")
            ser_data = user_schema.dump(user)
            token = Authentication.generate_token(ser_data.get("id"))
            #return custom_response({"jwt_token": token}, 200)
            return render_template("index.html", title="Welcom to Python Flask RESTful API")
        except ValidationError as err:
            errors = err.messages
            valid_data = err.valid_data	
            print(f"create() error! {errors}")		
            return render_template("login.html", title="Welcom to Python Flask RESTful API", error=errors)
    return render_template("login.html", title="Welcom to Python Flask RESTful API")