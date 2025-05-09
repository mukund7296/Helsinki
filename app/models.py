from app import mongo

def get_all_songs(page=1, per_page=5):
    skip = (page - 1) * per_page
    return list(mongo.db.songs.find().skip(skip).limit(per_page))

def get_avg_difficulty(level=None):
    match = {"level": level} if level else {}
    pipeline = [{"$match": match}, {"$group": {"_id": None, "avgDifficulty": {"$avg": "$difficulty"}}}]
    result = list(mongo.db.songs.aggregate(pipeline))
    return result[0]["avgDifficulty"] if result else None

def search_songs(message):
    query = {"$or": [
        {"artist": {"$regex": message, "$options": "i"}},
        {"title": {"$regex": message, "$options": "i"}}
    ]}
    return list(mongo.db.songs.find(query))

def add_rating(song_id, rating):
    if not 1 <= rating <= 5:
        raise ValueError("Rating must be between 1 and 5")
    mongo.db.ratings.insert_one({"song_id": song_id, "rating": rating})

def get_song_ratings(song_id):
    pipeline = [
        {"$match": {"song_id": song_id}},
        {
            "$group": {
                "_id": "$song_id",
                "avg": {"$avg": "$rating"},
                "min": {"$min": "$rating"},
                "max": {"$max": "$rating"}
            }
        }
    ]
    result = list(mongo.db.ratings.aggregate(pipeline))
    return result[0] if result else {}
