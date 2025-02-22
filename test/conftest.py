import pytest
import os, sys
from src.main import app
from os.path import dirname, join, abspath
sys.path.insert(0, abspath(join(dirname(__file__), '../src')))

@pytest.fixture
def client():
    return app.test_client()

def pytest_generate_tests(metafunc):
    os.environ['JWT_SECRET_KEY'] = 'pythonflaskrestapipostgres'