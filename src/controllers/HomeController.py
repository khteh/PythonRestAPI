from flask import request, json, Response, Blueprint, render_template, flash, g, session
from datetime import datetime
from ..config import app_config
from ..common.Authentication import Authentication
from ..models.UserModel import UserModel
import re
home_api = Blueprint("home", __name__)
@home_api.context_processor
def inject_now():
    return {'now': datetime.utcnow()}

@home_api.route("/")
@home_api.route("/index")
def index():
    #print("homeController hello")
    greeting = None
    now = datetime.now()
    # https://www.programiz.com/python-programming/datetime/strftime
    formatted_now = now.strftime("%A, %d %B, %Y at %X")
    #if request.method == "POST":
    user = None
    if "logged_in" not in session or not session["logged_in"] or "token" not in session or not session["token"]:
        greeting = "Friend! It's " + formatted_now
        #print(f"homeController hello greeting: {greeting}")
        return render_template("index.html", title="Welcome to Python Flask RESTful API", greeting=greeting)	
    data = Authentication.decode_token(session["token"])
    if data["error"]:
        return render_template("login.html", title="Welcome to Python Flask RESTful API", error=data["error"])
    user_id = data["data"]["user_id"]
    print(f"User: {user_id}")
    user = UserModel.get_user(user_id)
    if not user:
        return render_template("login.html", title="Welcome to Python Flask RESTful API", error="Invalid user!")           
    try:
        print("Get user name...")
        print(f"Firstname: {user.firstname}, Lastname: {user.lastname}")
        name = user.firstname + ", " + user.lastname
        # Filter the name argument to letters only using regular expressions. URL arguments
        # can contain arbitrary text, so we restrict to safe characters only.
        match_object = re.match("[a-zA-Z ]+", name)
        if match_object:
            clean_name = match_object.group(0)
        else:
            clean_name = "Friend!"
        greeting = f"Hello {clean_name}! It's {formatted_now}"
        """Renders a homes page."""
    except (Exception) as error:
        greeting = "Exception {0}".format(error)
    if not greeting:
        greeting = "Friend! It's " + formatted_now
        #print(f"homeController hello greeting: {greeting}")
    return render_template("index.html", title="Welcome to Python Flask RESTful API", greeting=greeting)