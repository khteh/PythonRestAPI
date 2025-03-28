import pytest, sys, asyncio
import os, sys
from os.path import dirname, join, abspath
sys.path.insert(0, abspath(join(dirname(__file__), '../src')))
pytest_plugins = ('pytest_asyncio',)

@pytest.fixture(scope="function")
async def app_context():
    os.environ["Testing"] = True
    from src.main import app
    async with app.app_context() as app_context:
        app.config["WTF_CSRF_ENABLED"] = False
        yield app_context

def pytest_generate_tests(metafunc):
    """ called once per each test function """
    os.environ['JWT_SECRET_KEY'] = 'pythonflaskrestapipostgres'