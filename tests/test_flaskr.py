import pytest
from flaskr import create_app

@pytest.fixture
def client():
    app = create_app()
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_index(client):
    response = client.get('/')
    assert response.status_code == 200
    assert b'Welcome to Flaskr' in response.data

def test_index_with_name(client):
    response = client.get('/?name=World')
    assert response.status_code == 200
    assert b'World' in response.data