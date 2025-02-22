import pytest, sys, asyncio
from hypercorn.config import Config
from hypercorn.asyncio import serve
from os.path import dirname, join, abspath
from src.app import create_app
#from src.main import app
from quart_cors import cors
sys.path.insert(0, abspath(join(dirname(__file__), '../src')))
from common.Authentication import Authentication
pytest_plugins = ('pytest_asyncio',)

@pytest.fixture()
async def app_context():
    config = Config()
    config.bind = ["localhost:4433"]
    config.insecure_bind = ["localhost:8080"]
    config.worker_class = "asyncio"
    config.alt_svc_headers = ["h3=\":443\"; ma=3600, h3-29=\":443\"; ma=3600"]
    config.loglevel = "DEBUG"
    config.quic_bind = ["localhost:4433"]
    app = create_app()
    app = cors(app, allow_credentials=True, allow_origin="https://localhost:4433")
    asyncio.run(serve(app, config))
    async with app.app_context() as app_context:
        yield app_context    
@pytest.mark.asyncio
async def test_tokengeneration_pass(app_context):
    """ JWT token generation should pass with valid user input parameter """
    token = Authentication.generate_token("test_user")
    assert type(token) is str
    assert token != ""
@pytest.mark.asyncio
async def test_tokengeneration_fail(app_context):
    """ JWT token generation should fail without valid user input parameter """
    with pytest.raises(Exception) as e:
        token = Authentication.generate_token("")
    assert "Invalid user id!" in str(e.value)
@pytest.mark.asyncio
async def test_tokendecoding_pass(app_context):
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
@pytest.mark.asyncio
async def test_tokendecoding_fail(app_context):
    """ JWT token decoding should fail without valid user input parameter """
    with pytest.raises(Exception) as e:
        token = Authentication.decode_token("")
    assert "Invalid token!" in str(e.value)