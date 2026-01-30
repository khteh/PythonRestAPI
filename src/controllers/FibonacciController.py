import jsonpickle, logging
from quart import request, session, Blueprint, flash, session
from quart import (
    Blueprint,
    Response,
    ResponseReturnValue,
    current_app,
    make_response,
    render_template,
    session
)
from quart.utils import run_sync
from datetime import datetime, timezone
from array import array
from ..common.Response import custom_response
from ..common.Authentication import Authentication
from ..common.ResponseHelper import Respond
from ..models.UserModel import UserModel
from urllib.parse import urlparse, parse_qs
fibonacci_api = Blueprint("fibonacci", __name__)
@fibonacci_api.context_processor
def inject_now():
    return {'now': datetime.now(timezone.utc)}

@fibonacci_api.route("/", methods=["GET", "POST"])
async def fibonacci() -> ResponseReturnValue:
    fibonacci = None
    error = None
    user = None
    if "user" in session and session["user"]:
        user = session['user']
        logging.debug(f"session['user']: {user}")
        if user and "token" in user:
            data = Authentication.decode_token(user['token'])
            if data["error"]:
                logging.error(data["error"])
                await flash(data["error"])
                return await Respond("login.html", title="Welcome to Python Flask RESTful API", error=data["error"])
            logging.debug(f"data: {data}")
            user_id = data["data"]["user_id"]
            logging.debug(f"User: {user_id}")
            user = UserModel.get_user(user_id)
            if not user:
                logging.error(f"Invalid user {user_id}!")
                await flash(f"Invalid user {user_id}!")
                return await Respond("login.html", title="Welcome to Python Flask RESTful API", error="Invalid user!")
    if request.method == "POST":
        data = await request.get_data()
        params = parse_qs(data.decode('utf-8'))
        logging.debug(f"data: {data}, params: {params}")
        if 'n' in params and len(params['n']) and params["n"][0].strip() and params["n"][0].strip().isdigit():
            n = int(params["n"][0].strip())
            logging.debug(f"fibonacci(): {n}")
            try:
                fibonacci = f"Hello {('there' if not user else user.firstname)}, fibonacci({n}): {await run_sync(_fib)(n)}"
            except Exception as error:
                logging.exception(f"fibonacci() exception! {error}")
                await flash(f"Fibonacci {n} failed! {error}", "danger")
                #return await Respond("fibonacci.html", title="Welcome to Python Flask Fibonacci calculator")
                return await Respond("fibonacci.html", title="Welcome to Python Flask Fibonacci calculator")
        if not fibonacci:
            #error = custom_response({"error": "Please provide an 'N' for the fibonacci number!"}, 400)
            await flash("Please provide a numeric value 'N' for the fibonacci number!", "danger")
    return await Respond("fibonacci.html", title="Welcome to Python Flask Fibonacci calculator", fibonacci=fibonacci)

def _fib(n):
#    n = input(n)
#    if n.isnumeric():
    if n <= 1:
        return n
    else:
        #return fib(n-2) + fib(n-1)
        result = array('Q', [0,1]) # https://docs.python.org/3/library/array.html
        for i in range(2, n+1):
            result[i % 2] = result[(i - 2) % 2] + result[(i - 1) % 2]
        return result[n % 2]
