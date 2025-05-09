from flask import Blueprint, jsonify
from . import mongo

songs_bp = Blueprint("songs", __name__)

@songs_bp.route("/songs", methods=["GET"])
def get_songs():
    songs = list(mongo.db.songs.find({}, {"_id": 0}))
    return jsonify(songs)
