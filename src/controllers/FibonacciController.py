from flask import request, json, Response, Blueprint
from datetime import datetime
from ..config import app_config
from ..common.Response import custom_response
import re
fibonacci_api = Blueprint("fibonacci", __name__)

@fibonacci_api.route("/")
def fibonacci():
    print("FibonacciController fibonacci")
    content = None
    if "n" in request.args:
        n = request.args.get("n")
        if n and n.strip():
            if n.isnumeric():
                try:
                    content = "Hello there, fibonacci(" + n + "): " + str(fib(int(n)))
                    """Renders a greetings page."""
                except (Exception) as error:
                    content = "Exception {0}".format(error)
    if not content:
        return custom_response({"error": "Please provide an 'N' for the fibonacci number!"}, 400)
    return content

def fib(n):
#    n = input(n)
#    if n.isnumeric():
        if n <= 1:
            return n
        else:
            return fib(n-2) + fib(n-1)