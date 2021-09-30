import jwt, datetime, logging
from quart import json, Response, session, redirect, url_for, session, flash, abort, current_app
from flask_oidc import OpenIDConnect
from functools import wraps
from ..models.UserModel import UserModel
oidc = OpenIDConnect()
# https://github.com/jpadilla/pyjwt/blob/master/docs/usage.rst
class Authentication():
    """
    Authentication
    """
    @staticmethod
    def generate_token(user_id):
        """
        Generate Token
        """
        #print(f"generate_token(): user_id: {user_id}")
        if not current_app.config["JWT_SECRET_KEY"]:
            raise Exception("Invalid user id!")
        if user_id:
            try:
                now = datetime.datetime.utcnow()
                # https://pyjwt.readthedocs.io/en/latest/usage.html#registered-claim-names
                payload = {
                    "exp": now + datetime.timedelta(hours=1),
                    "iat": now,
                    "nbf": now,
                    "iss": "urn:PythonFlaskRestAPI",
					"aud": "urn:PythonFlaskRestAPI",
                    "user_id": user_id
					# https://stackoverflow.com/questions/28418360/jwt-json-web-token-audience-aud-versus-client-id-whats-the-difference
                }
                return jwt.encode(payload, current_app.config["JWT_SECRET_KEY"], "HS512")
            except Exception as e:
                print("generate_token() exception!")
                print(type(e))    # the exception instance
                print(e.args)     # arguments stored in .args
                print(e)          # __str__ allows args to be printed directly,
                                  # but may be overridden in exception subclasses
                return Response(mimetype="application/json", response=json.dumps({"error": "Token generation error!"}), status=400)
        else:
            raise Exception("Invalid user id!")
    @staticmethod
    def decode_token(token):
        """
        Decode Authentication Token
        """
        result = {"data": {}, "error": {}}
        if token:
            try:
                payload = jwt.decode(token, current_app.config["JWT_SECRET_KEY"], "HS512", audience="urn:PythonFlaskRestAPI")
                result["data"] = {"user_id": payload["user_id"]}
                return result
            except jwt.ExpiredSignatureError as expired:
                result["error"] = {"message": "Token expired! Please login again!"}
                return result
            except jwt.InvalidAudienceError as audError:
                result["error"] = {"message": "Invalid Audience! Please login again!"}
                print("InvalidAudienceError!")
            except jwt.InvalidTokenError as invalid:
                result["error"] = {"message": "Invalid Token! Please login again!"}
                return result
        else:
            raise Exception("Invalid token!")
    @staticmethod
    def auth_required(url):
        def actual_auth_required(func):
            """
            Authentication required
            """
            @wraps(func)
            def decorated_auth_required(*args, **kwargs):
                session["url"] = url_for(url, *args, **kwargs) if url else url
                #if "api-token" not in request.headers:
                if "user" not in session or not session["user"] or not session["user"]["token"]:
                    #await flash(f"Please login to continue.", "info")
                    return redirect(url_for("auth.login"))
                #token = request.headers.get("api-token")
                data = Authentication.decode_token(session["user"]["token"])
                if data["error"]:
                    logging.warning(f"[Auth] error: {data['error']}!")                
                    #await flash(f"{data['error']}", "danger")
                    return redirect(url_for("auth.login"))
                user_id = data["data"]["user_id"]
                check_user = UserModel.get_user(user_id)
                if not check_user:
                    logging.warning(f"[Auth] Invalid user {user_id}!")
                    #await flash(f"Invalid username and/or password!", "danger")
                    return redirect(url_for("auth.login"))
                return func(*args, **kwargs)
            return decorated_auth_required
        return actual_auth_required

    @staticmethod
    def isAuthenticated():
        return oidc.user_loggedin and "user" in session and "token" in session["user"]

    @staticmethod
    def require_role(role):
        def decorated_require_role(func):
            @wraps(func)
            def wrapped_require_role(*args, **kwargs):
                if Authentication.isAuthenticated() and role in session["user"]["roles"]:
                    return func(*args, **kwargs)
                else:
                    return abort(403)
            return wrapped_require_role
        return decorated_require_role
