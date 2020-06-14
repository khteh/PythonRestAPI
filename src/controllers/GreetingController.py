from flask import request, json, Response, Blueprint
from datetime import datetime
from ..config import app_config
import re
greeting_api = Blueprint("greeting", __name__)

@greeting_api.route("/")
def hello():
    #print("GreetingController hello")
    now = datetime.now()
    # https://www.programiz.com/python-programming/datetime/strftime
    formatted_now = now.strftime("%A, %d %B, %Y at %X")
    content = None
    if "name" in request.args:
        name = request.args.get("name")
        if name and name.strip():
            try:
                # Filter the name argument to letters only using regular expressions. URL arguments
                # can contain arbitrary text, so we restrict to safe characters only.
                match_object = re.match("[a-zA-Z]+", name)
                if match_object:
                    clean_name = match_object.group(0)
                else:
                    clean_name = "Friend!"
                content = "Hello there, " + clean_name + "! It's " + formatted_now
                """Renders a greetings page."""
            except (Exception) as error:
                content = "Exception {0}".format(error)
    if not content:
        content = "Friend! It's " + formatted_now
        #print(f"GreetingController hello content: {content}")
    return content