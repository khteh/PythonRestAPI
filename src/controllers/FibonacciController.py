from flask import request, json, Response, Blueprint, flash, render_template, session
from datetime import datetime
from array import array
from ..config import app_config
from ..common.Response import custom_response
from ..common.Authentication import Authentication
from ..models.UserModel import UserModel
import re
fibonacci_api = Blueprint("fibonacci", __name__)
@fibonacci_api.context_processor
def inject_now():
    return {'now': datetime.utcnow()}

@fibonacci_api.route("/", methods=["GET", "POST"])
def fibonacci():
    fibonacci = None
    error = None
    user = None
    if "logged_in" in session and session["logged_in"] and "token" in session and session["token"]:
        data = Authentication.decode_token(session["token"])
        if data["error"]:
            return render_template("login.html", title="Welcome to Python Flask RESTful API", error=data["error"])
        user_id = data["data"]["user_id"]
        print(f"User: {user_id}")
        user = UserModel.get_user(user_id)
        if not user:
            return render_template("login.html", title="Welcome to Python Flask RESTful API", error="Invalid user!")
    if request.method == "POST":
        if request.form['n']:
            n = request.form["n"]
            if n and n.strip():
                if n.isnumeric():
                    try:
                        fibonacci = f"Hello {('there' if not user else user.firstname)}, fibonacci(" + n + "): " + str(fib(int(n)))
                        """Renders a greetings page."""
                    except (Exception) as error:
                        error = "Exception {0}".format(error)
                        flash(f"Fibonacci {n} failed! {error}", "error")
                        return render_template("fibonacci.html", title="Welcome to Python Flask Fibonacci calculator")
        if not fibonacci:
            #error = custom_response({"error": "Please provide an 'N' for the fibonacci number!"}, 400)
            flash("Please provide a numeric value 'N' for the fibonacci number!", "danger")
    return render_template("fibonacci.html", title="Welcome to Python Flask Fibonacci calculator", fibonacci=fibonacci)

def fib(n):
#    n = input(n)
#    if n.isnumeric():
        if n <= 1:
            return n
        else:
            #return fib(n-2) + fib(n-1)
            result = array('Q', [0,1])
            for i in range(2, n+1):
                result[i % 2] = result[(i - 2) % 2] + result[(i - 1) % 2]
            return result[n % 2]