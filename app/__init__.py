import os
from flask import Flask
from flask_pymongo import PyMongo
from flask_swagger_ui import get_swaggerui_blueprint

mongo = PyMongo()

def create_app(test_config=None):
    # Create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    
    # Load configuration
    if test_config is None:
        app.config.from_object('app.config.Config')
    else:
        app.config.update(test_config)
    
    # Initialize MongoDB
    mongo.init_app(app)
    
    # Register Swagger UI
    SWAGGER_URL = '/api/docs'
    API_URL = '/static/swagger.json'
    swaggerui_blueprint = get_swaggerui_blueprint(
        SWAGGER_URL,
        API_URL,
        config={
            'app_name': "Songs API"
        }
    )
    app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)
    
    # Import and register routes
    from app.routes import songs_bp
    app.register_blueprint(songs_bp)
    
    # Create static folder if it doesn't exist
    os.makedirs(os.path.join(app.root_path, 'static'), exist_ok=True)
    
    # Generate Swagger JSON
    with open(os.path.join(app.root_path, 'static', 'swagger.json'), 'w') as f:
        f.write(generate_swagger_json())
    
    return app

def generate_swagger_json():
    return """{
  "swagger": "2.0",
  "info": {
    "title": "Songs API",
    "description": "API for managing songs and ratings",
    "version": "1.0.0"
  },
  "basePath": "/api",
  "schemes": [
    "http"
  ],
  "consumes": [
    "application/json"
  ],
  "produces": [
    "application/json"
  ],
  "paths": {
    "/songs": {
      "get": {
        "summary": "Get all songs",
        "parameters": [
          {
            "name": "page",
            "in": "query",
            "description": "Page number",
            "required": false,
            "type": "integer",
            "default": 1
          },
          {
            "name": "per_page",
            "in": "query",
            "description": "Number of songs per page",
            "required": false,
            "type": "integer",
            "default": 10
          }
        ],
        "responses": {
          "200": {
            "description": "A list of songs"
          }
        }
      }
    },
    "/songs/avg_difficulty": {
      "get": {
        "summary": "Get average difficulty of all songs",
        "parameters": [
          {
            "name": "level",
            "in": "query",
            "description": "Filter by level",
            "required": false,
            "type": "integer"
          }
        ],
        "responses": {
          "200": {
            "description": "Average difficulty"
          }
        }
      }
    },
    "/songs/search": {
      "get": {
        "summary": "Search songs by artist or title",
        "parameters": [
          {
            "name": "message",
            "in": "query",
            "description": "Search string",
            "required": true,
            "type": "string"
          }
        ],
        "responses": {
          "200": {
            "description": "List of songs matching the search criteria"
          },
          "400": {
            "description": "Missing required parameter"
          }
        }
      }
    },
    "/songs/{song_id}/rating": {
      "post": {
        "summary": "Add a rating to a song",
        "parameters": [
          {
            "name": "song_id",
            "in": "path",
            "description": "Song ID",
            "required": true,
            "type": "string"
          },
          {
            "name": "rating",
            "in": "body",
            "description": "Rating value",
            "required": true,
            "schema": {
              "type": "object",
              "properties": {
                "rating": {
                  "type": "number",
                  "minimum": 1,
                  "maximum": 5
                }
              }
            }
          }
        ],
        "responses": {
          "201": {
            "description": "Rating added successfully"
          },
          "400": {
            "description": "Invalid rating value"
          },
          "404": {
            "description": "Song not found"
          }
        }
      },
      "get": {
        "summary": "Get rating statistics for a song",
        "parameters": [
          {
            "name": "song_id",
            "in": "path",
            "description": "Song ID",
            "required": true,
            "type": "string"
          }
        ],
        "responses": {
          "200": {
            "description": "Rating statistics"
          },
          "404": {
            "description": "Song not found or no ratings available"
          }
        }
      }
    }
  }
}"""
