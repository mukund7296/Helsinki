

# 🎵 Songs API

This is a Flask + MongoDB API to manage songs and ratings data.

# Helsinki Task- Song Api
Helsinki/
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
git clone https://github.com/mukund7296/songs-api.git
cd songs-api

# Run the services
docker-compose up --build

Access API at: http://localhost:5000



📁 Data Import
Run this after MongoDB container starts:

bash
Copy
Edit
docker exec -i songs_db mongoimport --db songs_db --collection songs --jsonArray --file /data.json --drop
If local:

bash
Copy
Edit
mongoimport --db songs_db --collection songs --jsonArray --file data.json --drop
🧪 Running Tests
bash
Copy
Edit
docker exec -it <container_id_or_name> pytest
Or locally:

bash
Copy
Edit
pytest
