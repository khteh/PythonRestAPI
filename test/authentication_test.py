import os, pytest, sys, asyncio
from os.path import dirname, join, abspath
sys.path.insert(0, abspath(join(dirname(__file__), '../src')))
os.environ["Testing"] = "True"
from common.Authentication import Authentication

def test_tokengeneration_pass(app_context):
    """ JWT token generation should pass with valid user input parameter """
    token = Authentication.generate_token("test_user")
    assert type(token) is str
    assert token != ""

def test_tokengeneration_fail(app_context):
    """ JWT token generation should fail without valid user input parameter """
    with pytest.raises(Exception) as e:
        token = Authentication.generate_token("")
    assert "Invalid user id!" in str(e.value)

def test_tokendecoding_pass(app_context):
    """ JWT token decoding should pass with valid user input parameter """
    token = Authentication.generate_token("test_user")
    assert type(token) is str
    assert token != ""
    decode = Authentication.decode_token(token)
    """ result["data"] = {"user_id": payload["user_id"], "error": {}} """
    assert decode != ""
    assert decode["data"]
    assert decode["data"]["user_id"]
    assert decode["data"]["user_id"] == "test_user"
    expect = dict(data=dict(user_id="test_user"), error=dict())
    assert decode == expect

def test_tokendecoding_fail(app_context):
    """ JWT token decoding should fail without valid user input parameter """
    with pytest.raises(Exception) as e:
        token = Authentication.decode_token("")
    assert "Invalid token!" in str(e.value)