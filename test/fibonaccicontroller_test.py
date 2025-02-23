import pytest, json
from quart import g, url_for
from datetime import datetime, timezone
from http import HTTPStatus
from http.cookies import SimpleCookie
@pytest.mark.asyncio
async def test_fibonacci_get_pass(client):
    headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml',
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'
    }    
    response = await client.get('/fibonacci', headers=headers, follow_redirects=True)
    assert response != ""
    assert len(response.headers.getlist('Set-Cookie'))
    assert response.headers.getlist('Set-Cookie')[0] != ""

@pytest.mark.asyncio
async def test_fibonacci_pass(client):
    headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml',
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'
    }    
    response = await client.get('/fibonacci', headers=headers, follow_redirects=True)
    #response = await client.post('/fibonacci', data={"n": 10, "csrf_token": g.csrf_token}, follow_redirects=True)
    response = await client.post(url_for('/fibonacci'), data=b'n=10', follow_redirects=True)
    assert response.headers['content-type'] == "text/html; charset=utf-8"
    assert response != ""
    assert response.status_code == HTTPStatus.OK, 'FibonacciController failed'
    json = await response.get_json()
    data = await response.get_data()
    print(f"response json: {json}")
    print(f"data: {data}")
    #strResponse = response.data.decode("utf-8")
    assert json != ""
    #assert strResponse == "Hello there, fibonacci(10): 55"

@pytest.mark.asyncio
async def test_big_fibonacci_pass(client):
    headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml',
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'
    }    
    response = await client.get('/fibonacci', headers=headers, follow_redirects=True)
    #response = await client.post('/fibonacci', data={"n": 90, "csrf_token": g.csrf_token}, follow_redirects=True)
    response = await client.post(url_for('/fibonacci'), data=b'n=90', follow_redirects=True)
    assert response.headers['content-type'] == "text/html; charset=utf-8"
    assert response != ""
    assert response.status_code == HTTPStatus.OK, 'FibonacciController failed'
    strResponse = response.data.decode("utf-8")	
    assert strResponse != ""
    assert strResponse == "Hello there, fibonacci(10): 2880067194370816120"

@pytest.mark.asyncio
async def test_fibonacci_fail(client):
    headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml',
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'
    }    
    response = await client.get('/fibonacci', headers=headers, follow_redirects=True)
    #response = await client.post('/fibonacci', data={"n": 90, "csrf_token": g.csrf_token}, follow_redirects=True)
    response = await client.post(url_for('/fibonacci'), follow_redirects=True)
    assert response.headers['content-type'] == "application/json"
    assert response != ""
    assert response.status_code == HTTPStatus.BAD_REQUEST, 'FibonacciController failed'
    #strResponse = response.data.decode("utf-8")	
    assert response.json == {'error': "Please provide an 'N' for the fibonacci number!"}, 'Improper response'
    #assert strResponse != ""
    #assert strResponse == "Please provide an 'N' for the fibonacci number!"