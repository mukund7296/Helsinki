import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # MongoDB Configuration
    MONGO_URI = os.environ.get('MONGO_URI', 'mongodb://localhost:27017/songs_db')
    
    # Application Configuration
    DEBUG = os.environ.get('FLASK_DEBUG', False)
    TESTING = False
    SECRET_KEY = os.environ.get('SECRET_KEY', 'dev_key')
    
    # Pagination defaults
    DEFAULT_PAGE = 1
    DEFAULT_PER_PAGE = 10
    MAX_PER_PAGE = 100

class TestConfig(Config):
    TESTING = True
    MONGO_URI = 'mongodb://localhost:27017/test_songs_db'
