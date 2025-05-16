import re, logging, jsonpickle, json
from quart import (
    Blueprint,
    flash,
    formparser,
    request,
    Response,
    ResponseReturnValue,
    current_app,
    make_response,
    redirect,
    render_template,
    session,
    url_for
)
from datetime import datetime, timezone
from marshmallow import ValidationError
from urllib.parse import urlparse, parse_qs
from uuid_extensions import uuid7, uuid7str
from google import genai
from google.genai import types
from src.config import config
from src.common.Authentication import Authentication
from src.common.ResponseHelper import Respond
from src.common.Response import custom_response
from src.utils.JsonString import is_json
chat_api = Blueprint("chat", __name__)

@chat_api.route("/")
@chat_api.route("/index")
async def index() -> ResponseReturnValue:
    greeting = None
    now = datetime.now()
    # https://www.programiz.com/python-programming/datetime/strftime
    formatted_now = now.strftime("%A, %d %B, %Y at %X")
    #if request.method == "POST":
    user = None
    if "user" not in session or not session["user"]:
        greeting = "Friend! It's " + formatted_now
        #print(f"homeController hello greeting: {greeting}")
        return await Respond("index.html", title="Welcome to LLM-RAG 💬", greeting=greeting)
    user = jsonpickle.decode(session['user'])
    if not user or not hasattr(user, 'token'):
        greeting = "Friend! It's " + formatted_now
        #print(f"homeController hello greeting: {greeting}")
        return await Respond("index.html", title="Welcome to LLM-RAG 💬", greeting=greeting)
    data = Authentication.decode_token(user.token)
    if data["error"]:
        return await Respond("login.html", title="Welcome to LLM-RAG 💬", error=data["error"])
    user_id = data["data"]["user_id"]
    logging.debug(f"User: {user_id}")
    """
    user = UserModel.get_user(user_id)
    if not user:
        return await Respond("login.html", title="Welcome to LLM-RAG 💬", error="Invalid user!")
    try:
        logging.debug(f"Firstname: {user.firstname}, Lastname: {user.lastname}")
        name = user.firstname + ", " + user.lastname
        # Filter the name argument to letters only using regular expressions. URL arguments
        # can contain arbitrary text, so we restrict to safe characters only.
        match_object = re.match("[a-zA-Z ]+", name)
        if match_object:
            clean_name = match_object.group(0)
        else:
            clean_name = "Friend!"
        greeting = f"Hello {clean_name}! It's {formatted_now}"
    except (Exception) as error:
        greeting = "Exception {0}".format(error)
    """
    if not greeting:
        greeting = "Friend! It's " + formatted_now
        #print(f"homeController hello greeting: {greeting}")
    return await Respond("index.html", title="Welcome to LLM-RAG 💬", greeting=greeting)

@chat_api.post("/invoke")
async def invoke():
    """
    Invoke the agent with user input to retrieve a final response.
    Use thread_id to persist and continue a multi-turn conversation.
    """
    if "user_id" not in session or not session["user_id"]:
        session["user_id"] = uuid7str()
    if "thread_id" not in session or not session["thread_id"]:
        session["thread_id"] = uuid7str()
    logging.info(f"/invoke session {session['thread_id']} {session['user_id']}")
    """
    If it is not curl, then the request must have come from the browser with form data. The following processes it.
    """
    form = await request.form
    prompt:str = None
    image = None
    #logging.debug(f"form: {form}")
    if "prompt" in form and form["prompt"] and len(form["prompt"]):
        prompt = form["prompt"]
    if "image" in form and form["image"] and len(form["image"]):
        image = form["image"]
    if not prompt or not len(prompt):
        await flash("Please input your query!", "danger") # https://quart.palletsprojects.com/en/latest/reference/source/quart.helpers.html
        return await Respond("chat.html", title="Welcome to LLM-RAG 💬", error="Invalid input!")
    # Expect a single string.
    try:
        client = genai.Client(api_key=config.GEMINI_API_KEY)
        response = await client.models.generate_content(
            model="gemini-2.0-flash",
            contents=[image, prompt]
        )
        logging.debug(f"/invoke prompt: {prompt}, response: {response.text}")
        return custom_response({"message": response.text}, 200)
    except Exception as e:
        logging.exception(f"Exception: {e}")
        await flash(f"Failed to process your message! {e.messages}", "danger")
        #return redirect(url_for("chat.index"))

