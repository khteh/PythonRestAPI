import pytest, sys, asyncio
import os, sys
from src.main import app
#from src.app import create_app
from hypercorn.config import Config
from hypercorn.asyncio import serve
from os.path import dirname, join, abspath
sys.path.insert(0, abspath(join(dirname(__file__), '../src')))
pytest_plugins = ('pytest_asyncio',)

@pytest.fixture(scope="function")
def client():
    return app.test_client()

@pytest.fixture(scope="function")
async def app_context():
    config = Config()
    config.bind = ["localhost:4433"]
    config.insecure_bind = ["localhost:8080"]
    config.worker_class = "asyncio"
    config.alt_svc_headers = ["h3=\":443\"; ma=3600, h3-29=\":443\"; ma=3600"]
    config.loglevel = "DEBUG"
    config.quic_bind = ["localhost:4433"]
    #app = create_app()
    #app = cors(app, allow_credentials=True, allow_origin="https://localhost:4433")
    #asyncio.run(serve(app, config))
    async with app.app_context() as app_context:
        yield app_context

def pytest_generate_tests(metafunc):
    """ called once per each test function """
    os.environ['JWT_SECRET_KEY'] = 'pythonflaskrestapipostgres'