import logging
from quart import request, json, Response, Blueprint, g, render_template, flash, session, redirect, url_for
from marshmallow import ValidationError
from datetime import datetime
from base64 import b64encode, b64decode, urlsafe_b64encode, urlsafe_b64decode
from ..models.UserModel import UserModel, UserSchema
from ..common.Authentication import Authentication
from ..common.Response import custom_response
from ..common.Authentication import oidc
auth_api = Blueprint("auth", __name__)
user_schema = UserSchema()
@auth_api.context_processor
def inject_now():
    return {'now': datetime.utcnow()}

@auth_api.route("/login", methods=["GET", "POST"])
async def login():
    """
    User Login
    """
    if request.method == "POST":
        try:
            form = await request.form
            req_data = {"email": form["username"], "password": form["password"]}
            data = user_schema.load(req_data, partial=True)
            if not data:
                message = {"error": "Invalid input!"}
                return await render_template("login.html", title="Welcome to Python Flask RESTful API", error="Invalid input!")
                #return custom_response(message, 400)
            if not data.get("email") or not data.get("password"):
                #return custom_response({"error": "You need an email and password to login"}, 400)
                return await render_template("login.html", title="Welcome to Python Flask RESTful API", error="You need an email and password to login")
            user = UserModel.get_user_by_email(data.get("email"))
            if not user:
                #return custom_response({"error": "Invalid user!"}, 400)
                logging.warning(f"[Auth] Invalid user {data.get('email')}!")
                return await render_template("login.html", title="Welcome to Python Flask RESTful API", error="Invalid user!")
            if not user.check_hash(data.get("password")):
                #return custom_response({"error": "Invalid email or password!"}, 400)
                logging.warning(f"[Auth] Invalid email or password {data.get('email')}!")
                return await render_template("login.html", title="Welcome to Python Flask RESTful API", error="Invalid email or password!")
            ser_data = user_schema.dump(user)
            token = Authentication.generate_token(ser_data.get("id"))
            session['logged_in'] = True
            session["token"] = token
            #return custom_response({"jwt_token": token}, 200)
            logging.info(f"[Auth] User {user.email} logged in")
            return redirect(url_for("home.index"))
        except ValidationError as err:
            errors = err.messages
            valid_data = err.valid_data
            logging.error(f"[Auth] login() error! {errors}")
            print(f"login() error! {errors}")		
            return await render_template("login.html", title="Welcome to Python Flask RESTful API", error=errors)
    return await render_template("login.html", title="Welcome to Python Flask RESTful API")

@auth_api.route("/login_oidc", methods=["GET", "POST"])
@oidc.require_login
async def login_oidc():
    """Example for protected endpoint that extracts private information from the OpenID Connect id_token.
       Uses the accompanied access_token to access a backend service.
    """
    if oidc.user_loggedin:
        try:
            info = oidc.user_getinfo(['preferred_username', 'email', 'sub'])
            username = info.get('preferred_username')
            email = info.get('email')
            user_id = info.get('sub')
            if user_id in oidc.credentials_store:
                try:
                    access_token = oidc.get_access_token()
                    pre, tkn, post = access_token.split('.')
                    tkn += "=" * ((4 - len(tkn) % 4) % 4)
                    token = json.loads(b64decode(tkn))
                    #print(f"token: {token}")
                    roles = token["realm_access"]["roles"]
                    headers = {'Authorization': 'Bearer %s' % (access_token)}
                    session["user"] = {"id": user_id, "username": username, "email": email, "token": access_token, "roles": roles}
                    # YOLO
                    #greeting = requests.get('http://localhost:8080/greeting', headers=headers).text
                    #return await render_template("index.html")
                    print(f"[Auth] UserId: {user_id}, UserName: {username}, Email: {email}, Roles: {roles}, Profile: {profile} logged in")
                    if "url" in session and session["url"]:
                        return redirect(session["url"])
                    else:
                        return redirect(url_for("home.index"))
                except Exception as e:
                    print(f"Login fails! {str(e)}")
                    return await render_template("login_error.html", error_message="Invalid credentials!")
            else:
                print(f"Invalid credentials!")
                return await render_template("login_error.html", error_message="Invalid credentials!")
        except Exception as e:
            print(f"Please login to continue. {str(e)}")
        return await render_template("login_error.html", error_message="Invalid credentials!")

@auth_api.route("/logout")
@Authentication.auth_required
async def logout():
    """
    User Logout
    """
    print(f"logout()")
    logging.info(f"[Auth] User {g.user['id']} logged out")	
    g.user = {}	
    session['logged_in'] = False
    session["token"] = ""
    return await render_template("login.html", title="Welcome to Python Flask RESTful API")

@auth_api.route('/logout_oidc')
@oidc.require_login
async def logout_oidc():
    """Performs local logout by removing the session cookie."""
    if oidc.user_loggedin and session["user"]:
        print(f"[Auth] UserId: {session['user']['id']}, UserName: {session['user']['username']}, Email: {session['user']['email']} logged out")
        oidc.logout()
        session["user"] = None
        session["url"] = None
    return redirect(url_for("home.index"))

@auth_api.route("/profile")
@Authentication.auth_required
async def profile():
    """
    Get my profile
    """
    user = UserModel.get_user(g.user['id'])
    if not user:
        raise Exception(f"User {g.user.get('id')} not found!")
    return custom_response(user_schema.dump(user), 200)
