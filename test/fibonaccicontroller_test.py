import pytest, json
from datetime import datetime, timezone
from http import HTTPStatus

@pytest.mark.asyncio
async def test_fibonacci_pass(client):
    #async with client.request("/fibonacci", method="POST") as connection:
    #    await connection.send(b"n=10", follow_redirects=True)
    #    await connection.send_complete()
    #response = await connection.as_response()
    response = await client.post('/fibonacci', data=b"n=10", follow_redirects=True)
    #print(f"FibonacciController response content-type: {response.headers['content-type']}, data: {response.data}")
    #print(response.__dict__)
    assert response.headers['content-type'] == "text/html; charset=utf-8"
    assert response != ""
    assert response.status_code == HTTPStatus.OK, 'FibonacciController failed'
    json = await response.get_json()
    data = await response.get_data()
    print(f"response json: {json}")
    print(f"data: {data}")
    #strResponse = response.data.decode("utf-8")	
    assert json != ""
    assert strResponse == "Hello there, fibonacci(10): 55"

@pytest.mark.asyncio
async def test_big_fibonacci_pass(client):
    response = await client.post("/fibonacci", data={'n': 90}, follow_redirects=True)
    #print(f"FibonacciController response content-type: {response.headers['content-type']}, data: {response.data}")
    #print(response.__dict__)
    assert response.headers['content-type'] == "text/html; charset=utf-8"
    assert response != ""
    assert response.status_code == HTTPStatus.OK, 'FibonacciController failed'
    strResponse = response.data.decode("utf-8")	
    assert strResponse != ""
    assert strResponse == "Hello there, fibonacci(10): 2880067194370816120"

@pytest.mark.asyncio
async def test_fibonacci_fail(client):
    response = await client.post('/fibonacci', follow_redirects=True)
    #print(f"FibonacciController response content-type: {response.headers['content-type']}, data: {response.data}")
    #print(response.__dict__)
    assert response.headers['content-type'] == "application/json"
    assert response != ""
    assert response.status_code == HTTPStatus.BAD_REQUEST, 'FibonacciController failed'
    #strResponse = response.data.decode("utf-8")	
    assert response.json == {'error': "Please provide an 'N' for the fibonacci number!"}, 'Improper response'
    #assert strResponse != ""
    #assert strResponse == "Please provide an 'N' for the fibonacci number!"