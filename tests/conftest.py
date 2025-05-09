import os
import json
import pytest
from app import create_app, mongo
from bson import ObjectId

@pytest.fixture
def app():
    """Create and configure a Flask app for testing."""
    test_config = {
        'TESTING': True,
        'MONGO_URI': 'mongodb://localhost:27017/test_songs_db',
        'DEFAULT_PAGE': 1,
        'DEFAULT_PER_PAGE': 10,
        'MAX_PER_PAGE': 100
    }
    
    app = create_app(test_config)
    
    with app.app_context():
        # Clear the test database
        mongo.db.songs.drop()
        
        # Load test data
        test_songs = [
            {
                "_id": ObjectId("5f50e1e5c7ba6b5a7c9b3b1e"),
                "artist": "Test Artist 1",
                "title": "Test Song 1",
                "difficulty": 10.5,
                "level": 9,
                "released": "2020-01-01",
                "ratings": [3, 4, 5]
            },
            {
                "_id": ObjectId("5f50e1e5c7ba6b5a7c9b3b1f"),
                "artist": "Test Artist 2",
                "title": "Test Song 2",
                "difficulty": 15.0,
                "level": 13,
                "released": "2020-02-01",
                "ratings": [2, 3]
            },
            {
                "_id": ObjectId("5f50e1e5c7ba6b5a7c9b3b2a"),
                "artist": "Another Artist",
                "title": "Another Song",
                "difficulty": 5.5,
                "level": 6,
                "released": "2020-03-01",
                "ratings": []
            }
        ]
        
        # Insert test data
        mongo.db.songs.insert_many(test_songs)
    
    yield app
    
    # Clean up after the tests
    with app.app_context():
        mongo.db.songs.drop()

@pytest.fixture
def client(app):
    """Create a test client for the app."""
    return app.test_client()
