# Songs API

A RESTful API for managing songs and ratings built with Flask and MongoDB.

## Features

- List songs with pagination
- Calculate average difficulty
- Search songs by artist and title
- Add ratings to songs
- Get rating statistics
- Swagger UI documentation
- Containerization with Docker
- Comprehensive test suite

## Requirements

To run this project locally without Docker, you'll need:

- Python 3.9+
- MongoDB 4.4+

## Project Structure

```
songs-api/
│
├── app/                  # Application package
│   ├── __init__.py       # App initialization and factory
│   ├── config.py         # Configuration settings
│   ├── models.py         # Data models
│   ├── routes.py         # API routes
│   └── utils.py          # Utility functions
│
├── tests/                # Test suite
│   ├── __init__.py
│   ├── conftest.py       # Pytest fixtures
│   └── test_routes.py    # Route tests
│
├── Dockerfile            # Docker configuration
├── docker-compose.yml    # Docker Compose configuration
├── requirements.txt      # Python dependencies
├── run.py                # Application entry point
├── songs.json            # Seed data
└── README.md             # This file
```

## API Routes

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/songs` | GET | Get all songs with pagination |
| `/api/songs/avg_difficulty` | GET | Get average difficulty (optional `level` filter) |
| `/api/songs/search` | GET | Search songs by artist or title (requires `message` parameter) |
| `/api/songs/:song_id/rating` | POST | Add a rating to a song |
| `/api/songs/:song_id/rating` | GET | Get rating statistics for a song |

## Installation and Setup

### Option 1: Using Docker (Recommended)

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd songs-api
   ```

2. Make sure you have Docker and Docker Compose installed.

3. Start the application:
   ```bash
   docker-compose up -d
   ```

4. The API will be available at http://localhost:5000/api/
   Swagger documentation is available at http://localhost:5000/api/docs/

### Option 2: Local Setup

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd songs-api
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Start MongoDB (or use Docker for MongoDB only):
   ```bash
   docker run --detach --name songs_db --publish 127.0.0.1:27017:27017 mongo:4.4
   ```

5. Run the application:
   ```bash
   python run.py
   ```

6. The API will be available at http://localhost:5000/api/
   Swagger documentation is available at http://localhost:5000/api/docs/

## Running Tests

To run the test suite:

```bash
pytest
```

For more detailed output:

```bash
pytest -v
```

For test coverage:

```bash
pytest --cov=app tests/
```

## Design Decisions

### Scalability Considerations

The API is designed to handle a large number of songs and ratings:

- **Pagination**: All endpoints that return lists support pagination to prevent excessive data loading.
- **Indexing**: The application creates indexes on fields used for searching, filtering, and sorting.
- **Aggregation Framework**: MongoDB's aggregation pipeline is used for efficient calculations.
- **Query Optimization**: Queries are designed to minimize data transfer between the database and application.

### Performance Optimizations

- **Text Indexes**: Created for efficient text search operations
- **Field Projection**: Only required fields are fetched from the database
- **Document Structure**: Ratings are stored in an array within the song document for efficient statistics calculations

## API Documentation

Swagger UI documentation is available at `/api/docs/` when the application is running.
