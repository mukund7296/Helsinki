from flask import Blueprint, request, jsonify
from app.models import *

main = Blueprint('main', __name__)

@main.route("/songs", methods=["GET"])
def songs():
    page = int(request.args.get("page", 1))
    per_page = int(request.args.get("per_page", 5))
    return jsonify(get_all_songs(page, per_page))

@main.route("/difficulty/average", methods=["GET"])
def avg_difficulty():
    level = request.args.get("level", type=int)
    return jsonify({"average_difficulty": get_avg_difficulty(level)})

@main.route("/songs/search", methods=["GET"])
def search():
    msg = request.args.get("message")
    if not msg:
        return jsonify({"error": "Missing message param"}), 400
    return jsonify(search_songs(msg))

@main.route("/songs/rate", methods=["POST"])
def rate():
    data = request.get_json()
    try:
        add_rating(data["song_id"], int(data["rating"]))
        return jsonify({"message": "Rating added"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@main.route("/songs/<song_id>/ratings", methods=["GET"])
def ratings(song_id):
    return jsonify(get_song_ratings(song_id))
