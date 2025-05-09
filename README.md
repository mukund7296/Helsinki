

# 🎵 Songs API

This is a Flask + MongoDB API to manage songs and ratings data.

# Helsinki Task
songs-api/
├── app/
│   ├── __init__.py
│   ├── models.py
│   ├── routes.py
│   └── utils.py
├── tests/
│   └── test_api.py
├── data.json
├── Dockerfile
├── requirements.txt
├── run.py
├── README.md
└── docker-compose.yml

## 🚀 Features

- List all songs with pagination
- Average difficulty (with optional level filter)
- Case-insensitive search by artist/title
- Rate a song (1–5)
- Retrieve rating stats (avg, min, max)

## 🐳 Running with Docker

```bash
# Clone the repository
git clone https://github.com/your-repo/songs-api.git
cd songs-api

# Run the services
docker-compose up --build
