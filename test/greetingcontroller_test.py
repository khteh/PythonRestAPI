import pytest, json
from datetime import datetime
from http import HTTPStatus
def test_hello_pass(client):
    now = datetime.now()
    # https://www.programiz.com/python-programming/datetime/strftime
    formatted_now = now.strftime("%A, %d %B, %Y at %X")
    response = client.get('/api/v1/greeting/')
    #print(f"GreetingController response content-type: {response.headers['content-type']}, data: {response.data}")
    #print(response.__dict__)
    assert response.headers['content-type'] == "text/html; charset=utf-8"
    assert response != ""
    assert response.status_code == HTTPStatus.OK, 'GreetingController failed'
    strResponse = response.data.decode("utf-8")	
    assert strResponse != ""
    assert strResponse == "Friend! It's " + formatted_now