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
from quart_uploads import UploadSet, FE
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
from src.models.schema import UserInput
from src.models.ReceiptModel import ReceiptModel
from src.models.ContentModal import ContentModal
from src.utils.JsonString import is_json
chat_api = Blueprint("chat", __name__)
images = UploadSet('images', FE.Images)

@chat_api.context_processor
def inject_now():
    return {'now': datetime.now(timezone.utc)}

@chat_api.get("/")
@chat_api.get("/index")
async def index() -> ResponseReturnValue:
    logging.info(f"\n=== /chat/index ===")
    greeting = None
    now = datetime.now()
    # https://www.programiz.com/python-programming/datetime/strftime
    formatted_now = now.strftime("%A, %d %B, %Y at %X")
    #if request.method == "POST":
    user = None
    if "user" not in session or not session["user"]:
        greeting = "Friend! It's " + formatted_now
        return await Respond("chat.html", title="Welcome to LLM-RAG 💬", greeting=greeting)
    user = jsonpickle.decode(session['user'])
    if not user or not hasattr(user, 'token'):
        greeting = "Friend! It's " + formatted_now
        #print(f"ChatController hello greeting: {greeting}")
        return await Respond("chat.html", title="Welcome to LLM-RAG 💬", greeting=greeting)
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
        #print(f"ChatController hello greeting: {greeting}")
    return await Respond("chat.html", title="Welcome to LLM-RAG 💬", greeting=greeting)

async def ProcessCurlInput() -> UserInput:
    """
    This process curl post body:
    c3 -v https://10.152.183.176/invoke -XPOST -d '{"message": "What is task decomposition?"}'
    """
    data = await request.get_data()
    logging.debug(f"ProcessCurlInput(): data: {data}")
    params = parse_qs(data.decode('utf-8'))
    user_input: UserInput = None
    if is_json(data):
        user_input = json.loads(data)
    elif isinstance(params, dict):
        str_params: str = json.dumps(params)
        if str_params and len(str_params) and is_json(str_params):
            user_input = json.loads(str_params)
    return user_input

async def ProcessReceipt(image):
    try:
        logging.debug(f"\n=== {ProcessReceipt.__name__} ===")
        client = genai.Client(api_key=config.GEMINI_API_KEY)
        prompt:str = """
                        Process the image by extracting the following information and return the result in JSON format:
                        Date
                        Currency (3-character currency code)
                        Vendor
                        Items (array):
                        - Name
                        - Amount
                        GST/tax (One GST/tax for the entire receipt)
                        Total
                      """
        """
      inlineData: {
        data: image.buffer.toString('base64'),
        mimeType: image.mimetype.toString(),
      },
        """
        data: ContentModal = ContentModal(data = image.read(), mimeType = image.content_type)
        logging.debug(f"data: {len(data.data)}, mime: {data.mimeType}")
        if data.data and len(data.data) and data.mimeType and len(data.mimeType):          
            response = client.models.generate_content(
                model="gemini-2.0-flash",
                contents=[prompt, data],
                config={
                    "response_mime_type": "application/json",
                    "response_schema": ReceiptModel,
                },
            )
            receipt: ReceiptModel = response.parsed
            logging.debug(f"{ProcessReceipt.__name__} response: {response.text}, receipt: {receipt}")
            return custom_response({"message": response.text}, 200)
        else:
            await flash("Invalid image!", "danger") # https://quart.palletsprojects.com/en/latest/reference/source/quart.helpers.html
            return await Respond("chat.html", title="Welcome to LLM-RAG 💬", error="Invalid input!")
    except ValueError as v:
        logging.exception(f"Exception: {v}")
        await flash(f"Failed to process your message! {v}", "danger")
    except Exception as e:
        logging.exception(f"Exception: {e}")
        await flash(f"Failed to process your message! {e.messages}", "danger")
    return await Respond("chat.html", title="Welcome to LLM-RAG 💬", error="Invalid input!")

@chat_api.post("/invoke")
async def invoke():
    """
    Invoke the agent with user input to retrieve a final response.
    Use thread_id to persist and continue a multi-turn conversation.
    """
    logging.debug(f"\n=== {invoke.__name__} ===")
    if "user_id" not in session or not session["user_id"]:
        session["user_id"] = uuid7str()
    if "thread_id" not in session or not session["thread_id"]:
        session["thread_id"] = uuid7str()
    logging.info(f"/invoke session {session['thread_id']} {session['user_id']}")
    user_input: UserInput = None; # = await ProcessCurlInput()
    """
    If it is not curl, then the request must have come from the browser with form data. The following processes it.
    """
    prompt:str = None
    image = None
    isReceipt: bool = None
    if not user_input or "prompt" not in user_input:
        form = await request.form
        files = await request.files
        logging.debug(f"form: {form}, files: {files}")
        if "prompt" in form and form["prompt"] and len(form["prompt"]):
            prompt = form["prompt"]
        if "receipt" in form and form["receipt"]:
            isReceipt = form["receipt"]
        if "image" in files and files["image"]:
            image = files["image"]
    logging.debug(f"prompt: {prompt}, image: {image}, {type(image)}, receipt: {isReceipt}")
    if isReceipt:
        return await ProcessReceipt(image)
    """
    if not user_input or "prompt" not in user_input or not len(user_input["prompt"]):
        await flash("Please input your query!", "danger") # https://quart.palletsprojects.com/en/latest/reference/source/quart.helpers.html
        return await Respond("chat.html", title="Welcome to LLM-RAG 💬", error="Invalid input!")
    """
    if not prompt or not len(prompt):
        await flash("Please input your query!", "danger") # https://quart.palletsprojects.com/en/latest/reference/source/quart.helpers.html
        return await Respond("chat.html", title="Welcome to LLM-RAG 💬", error="Invalid input!")
    content = [prompt]
    if image:
        content.append(image)
    try:
        client = genai.Client(api_key=config.GEMINI_API_KEY)
        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=content
        )
        logging.debug(f"/invoke prompt: {prompt}, response: {response.text}")
        return custom_response({"message": response.text}, 200)
    except ValueError as v:
        logging.exception(f"Exception: {v}")
        await flash(f"Failed to process your message! {v}", "danger")   
    except Exception as e:
        logging.exception(f"Exception: {e}")
        await flash(f"Failed to process your message! {e.messages}", "danger")
    return await Respond("chat.html", title="Welcome to LLM-RAG 💬", error="Invalid input!")