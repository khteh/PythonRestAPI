from flask import request, json, Response, Blueprint, flash, render_template
from datetime import datetime
from array import array
from ..config import app_config
from ..common.Response import custom_response
import re
fibonacci_api = Blueprint("fibonacci", __name__)
@fibonacci_api.context_processor
def inject_now():
    return {'now': datetime.utcnow()}

@fibonacci_api.route("/", methods=["GET", "POST"])
def fibonacci():
    fibonacci = None
    error = None
    if request.method == "POST":
        if request.form['n']:
            n = request.form["n"]
            if n and n.strip():
                if n.isnumeric():
                    try:
                        fibonacci = "Hello there, fibonacci(" + n + "): " + str(fib(int(n)))
                        """Renders a greetings page."""
                    except (Exception) as error:
                        error = "Exception {0}".format(error)
        if not fibonacci:
            #error = custom_response({"error": "Please provide an 'N' for the fibonacci number!"}, 400)
            error = "Please provide an 'N' for the fibonacci number!"
            flash("Please provide an 'N' for the fibonacci number!")
    return render_template("fibonacci.html", title="Welcom to Python Flask Fibonacci calculator", fibonacci=fibonacci, error=error)

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