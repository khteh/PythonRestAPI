import pytest, json
from quart_wtf.utils import generate_csrf, validate_csrf, logger
from src.main import app
# CSRF: https://gist.github.com/singingwolfboy/2fca1de64950d5dfed72?permalink_comment_id=4556252
@pytest.mark.asyncio
async def test_fibonacci_get_pass(app_context):
    headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml',
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'
    }
    client = app.test_client()
    response = await client.get('/fibonacci', headers=headers, follow_redirects=True)
    assert response
    assert response.status_code == 200, 'FibonacciController failed'
    assert len(response.headers.getlist('Set-Cookie'))
    assert response.headers.getlist('Set-Cookie')[0] != ""

@pytest.mark.asyncio
async def test_fibonacci_pass(app_context):
    headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml',
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'
    }
    client = app.test_client()
    response = await client.get('/fibonacci', headers=headers, follow_redirects=True)
    response = await client.post('/fibonacci', data=b'n=90', follow_redirects=True)
    assert response.headers['content-type'] == "text/html; charset=utf-8"
    assert response
    assert response.status_code == 200, 'FibonacciController failed'
    data = await response.get_data()
    strResponse = data.decode("utf-8")
    assert strResponse != ""
    assert "Hello there, fibonacci(90): 2880067194370816120" in strResponse, "Invalid fibonacci(90) calculation response"

@pytest.mark.asyncio
async def test_fibonacci_fail(app_context):
    headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml',
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'
    }
    client = app.test_client()
    response = await client.get('/fibonacci', headers=headers, follow_redirects=True)
    response = await client.post('/fibonacci', follow_redirects=True)
    assert response.headers['content-type'] == "text/html; charset=utf-8"
    assert response
    assert response.status_code == 200, 'FibonacciController failed'
    data = await response.get_data()
    strResponse = data.decode("utf-8")
    assert strResponse != ""
    assert "Please provide a numeric value &#39;N&#39; for the fibonacci number!" in strResponse, 'Improper response'