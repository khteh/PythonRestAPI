from flask import request, json, Response, Blueprint, g
def custom_response(result, code):
    """
    Custom Response
    """
    return Response(mimetype="application/json", response=json.dumps(result), status=code)
