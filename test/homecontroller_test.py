import pytest, json
from datetime import datetime, timezone
from http import HTTPStatus
from bs4 import BeautifulSoup
from src.main import app
@pytest.mark.asyncio
async def test_hello_pass(app_context):
    now = datetime.now()
    # https://www.programiz.com/python-programming/datetime/strftime
    formatted_now = now.strftime("%A, %d %B, %Y at %X")
    client = app.test_client()
    response = await client.get('/')
    #print(f"GreetingController response content-type: {response.headers['content-type']}, data: {response.data}")
    #print(response.__dict__)
    assert response.headers['content-type'] == "text/html; charset=utf-8"
    assert response != ""
    assert response.status_code == HTTPStatus.OK, 'HomeController failed'
    data = await response.get_data()
    #print(f"response: {data}")
    assert data != ""
    html = BeautifulSoup(data, 'html.parser')
    assert html != ""
    text = html.get_text()
    assert text != ""
    #print(f"text: {text}")
    assert "Friend! It's " + formatted_now in text