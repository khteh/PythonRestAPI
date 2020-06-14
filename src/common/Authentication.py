import jwt
import os, sys
import datetime
from flask import json, Response, request, g
from functools import wraps
from ..models.UserModel import UserModel
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
        if not os.getenv("JWT_SECRET_KEY"):
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
                return jwt.encode(payload, os.getenv("JWT_SECRET_KEY"), "HS512").decode("utf-8")
            except Exception as e:
                print("generate_token exception!")
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
                payload = jwt.decode(token, os.getenv("JWT_SECRET_KEY"), audience="urn:PythonFlaskRestAPI")
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
    def auth_required(func):
        """
        Authentication required
        """
        @wraps(func)
        def decorated_auth_required(*args, **kwargs):
            if "api-token" not in request.headers:
                return Response(mimetype="application/json", response=json.dumps({"error": "Please login to continue!"}), status=400)
            token = request.headers.get("api-token")
            data = Authentication.decode_token(token)
            if data["error"]:
                return Response(mimetype="application/json", response=json.dumps(data["error"]), status=400)
            user_id = data["data"]["user_id"]
            check_user = UserModel.get_user(user_id)
            if not check_user:
                return Response(mimetype="application/json", response=json.dumps({"error": "Invalid user!"}), status=400)
            g.user = {"id": user_id}
            return func(*args, **kwargs)
        return decorated_auth_required