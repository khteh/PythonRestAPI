import pytest, json
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
    print(f"response headers: {response.headers}")
    for cookie in response.headers.getlist('Set-Cookie'):
        print(f"cookie: {cookie}")

@pytest.mark.asyncio
async def test_fibonacci_pass(client):
    headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml',
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'
    }    
    response = await client.get('/fibonacci', headers=headers, follow_redirects=True)
    cookie = SimpleCookie()
    cookie.load(response.headers.getlist('Set-Cookie')[0])
    #headers['cookie'] = response.headers.getlist('Set-Cookie')#'; '.join([x.name + '=' + x.value for x in response.cookies])
    headers['content-type'] = 'application/x-www-form-urlencoded'
    response = await client.post('/fibonacci', data=b'n=10', follow_redirects=True, headers=response.headers)
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