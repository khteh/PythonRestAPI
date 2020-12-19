import pytest, json
from datetime import datetime
from http import HTTPStatus
def test_fibonacci_pass(client):
    response = client.get('/api/v1/fibonacci?n=10', follow_redirects=True)
    #print(f"FibonacciController response content-type: {response.headers['content-type']}, data: {response.data}")
    #print(response.__dict__)
    assert response.headers['content-type'] == "text/html; charset=utf-8"
    assert response != ""
    assert response.status_code == HTTPStatus.OK, 'FibonacciController failed'
    strResponse = response.data.decode("utf-8")	
    assert strResponse != ""
    assert strResponse == "Hello there, fibonacci(10): 55"

def test_big_fibonacci_pass(client):
    response = client.get('/api/v1/fibonacci?n=90', follow_redirects=True)
    #print(f"FibonacciController response content-type: {response.headers['content-type']}, data: {response.data}")
    #print(response.__dict__)
    assert response.headers['content-type'] == "text/html; charset=utf-8"
    assert response != ""
    assert response.status_code == HTTPStatus.OK, 'FibonacciController failed'
    strResponse = response.data.decode("utf-8")	
    assert strResponse != ""
    assert strResponse == "Hello there, fibonacci(10): 2880067194370816120"

def test_fibonacci_fail(client):
    response = client.get('/api/v1/fibonacci', follow_redirects=True)
    #print(f"FibonacciController response content-type: {response.headers['content-type']}, data: {response.data}")
    #print(response.__dict__)
    assert response.headers['content-type'] == "application/json"
    assert response != ""
    assert response.status_code == HTTPStatus.BAD_REQUEST, 'FibonacciController failed'
    #strResponse = response.data.decode("utf-8")	
    assert response.json == {'error': "Please provide an 'N' for the fibonacci number!"}, 'Improper response'
    #assert strResponse != ""
    #assert strResponse == "Please provide an 'N' for the fibonacci number!"