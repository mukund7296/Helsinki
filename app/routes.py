from flask import Blueprint, request, jsonify, current_app
from app.models import Song
from app.utils import validate_rating, validate_pagination_params

# Create a Blueprint for song routes
songs_bp = Blueprint('songs', __name__, url_prefix='/api')

@songs_bp.route('/songs', methods=['GET'])
def get_songs():
    """
    Route A: Get all songs with pagination
    """
    # Get and validate pagination parameters
    page, per_page, error = validate_pagination_params(
        request.args.get('page', current_app.config['DEFAULT_PAGE'], type=int),
        request.args.get('per_page', current_app.config['DEFAULT_PER_PAGE'], type=int)
    )
    
    if error:
        return jsonify({'error': error}), 400
        
    songs = Song.get_all(page, per_page)
    
    return jsonify({
        'songs': songs,
        'page': page,
        'per_page': per_page,
        'total': len(songs)  # For small datasets; for large ones, use a count query
    })

@songs_bp.route('/songs/avg_difficulty', methods=['GET'])
def get_average_difficulty():
    """
    Route B: Get average difficulty of all songs
    Optional parameter 'level' to filter by level
    """
    level = request.args.get('level', type=int)
    avg_difficulty = Song.get_average_difficulty(level)
    
    if avg_difficulty is None:
        return jsonify({'error': 'No songs found'}), 404
        
    return jsonify({'average_difficulty': avg_difficulty})

@songs_bp.route('/songs/search', methods=['GET'])
def search_songs():
    """
    Route C: Search songs by artist or title
    Required parameter 'message' for search string
    """
    message = request.args.get('message')
    
    if not message:
        return jsonify({'error': 'Search message is required'}), 400
        
    songs = Song.search(message)
    
    return jsonify({'songs': songs})

@songs_bp.route('/songs/<song_id>/rating', methods=['POST'])
def add_rating(song_id):
    """
    Route D: Add a rating to a song
    """
    data = request.get_json()
    
    if not data or 'rating' not in data:
        return jsonify({'error': 'Rating is required'}), 400
        
    rating = data['rating']
    valid, error = validate_rating(rating)
    
    if not valid:
        return jsonify({'error': error}), 400
        
    success = Song.add_rating(song_id, rating)
    
    if not success:
        return jsonify({'error': 'Song not found'}), 404
        
    return jsonify({'message': 'Rating added successfully'}), 201

@songs_bp.route('/songs/<song_id>/rating', methods=['GET'])
def get_rating_stats(song_id):
    """
    Route E: Get rating statistics for a song
    """
    stats = Song.get_rating_stats(song_id)
    
    if not stats:
        return jsonify({'error': 'Song not found or no ratings available'}), 404
        
    return jsonify(stats)

@songs_bp.before_app_first_request
def initialize_database():
    """
    Initialize database with seed data
    """
    Song.seed_database()
