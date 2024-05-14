import pytest
from fastapi.testclient import TestClient
from uc_tools import HttpServer


@pytest.fixture
def client():
    server = HttpServer()
    return TestClient(server.app)


async def test_server(client):
    response = client.get('/health')
    assert response.status_code == 200
    assert response.text == 'OK'
