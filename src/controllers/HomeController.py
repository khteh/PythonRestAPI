from flask import request, json, Response, Blueprint, render_template, flash
from datetime import datetime
from ..config import app_config
import re
home_api = Blueprint("home", __name__)
@home_api.context_processor
def inject_now():
    return {'now': datetime.utcnow()}

@home_api.route("/", methods=["GET", "POST"])
@home_api.route("/index", methods=["GET", "POST"])
def index():
    #print("homeController hello")
    if request.method == "POST":
        now = datetime.now()
        # https://www.programiz.com/python-programming/datetime/strftime
        formatted_now = now.strftime("%A, %d %B, %Y at %X")
        greeting = None
        print(f"Name: {request.form['name']}")
        if request.form['name']:
            name = request.form["name"]
            if name and name.strip():
                try:
                    # Filter the name argument to letters only using regular expressions. URL arguments
                    # can contain arbitrary text, so we restrict to safe characters only.
                    match_object = re.match("[a-zA-Z ]+", name)
                    if match_object:
                        clean_name = match_object.group(0)
                    else:
                        clean_name = "Friend!"
                    greeting = "Hello there, " + clean_name + "! It's " + formatted_now
                    """Renders a homes page."""
                except (Exception) as error:
                    greeting = "Exception {0}".format(error)
        if not greeting:
            greeting = "Friend! It's " + formatted_now
            #print(f"homeController hello greeting: {greeting}")
        return render_template("index.html", title="Welcom to Python Flask RESTful API", greeting=greeting)
    return render_template("index.html", title="Welcom to Python Flask RESTful API")