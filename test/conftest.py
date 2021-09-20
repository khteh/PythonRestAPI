import pytest
import os, sys
from os.path import dirname, join, abspath
sys.path.insert(0, abspath(join(dirname(__file__), '../src')))
from flask import Flask

@pytest.fixture
def client():
    from app import create_app
    return create_app("development").test_client()

def pytest_generate_tests(metafunc):
        os.environ['JWT_SECRET_KEY'] = 'pythonflaskrestapipostgres'
