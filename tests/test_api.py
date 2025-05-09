import pytest
from app import create_app

@pytest.fixture
def client():
    app = create_app()
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client

def test_get_songs(client):
    res = client.get("/songs")
    assert res.status_code == 200

def test_search_missing_param(client):
    res = client.get("/songs/search")
    assert res.status_code == 400
