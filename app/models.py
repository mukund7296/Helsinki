
from bson import ObjectId
from app import mongo
from flask import current_app
import json

class Song:
    """Model for Song data"""
    
    @staticmethod
    def get_all(page=None, per_page=None):
        """
        Retrieve all songs with pagination
        
        Args:
            page (int): Page number
            per_page (int): Number of songs per page
            
        Returns:
            list: List of songs
        """
        if page is None:
            page = current_app.config['DEFAULT_PAGE']
        if per_page is None:
            per_page = current_app.config['DEFAULT_PER_PAGE']
            
        # Limit per_page to prevent excessive data loading
        per_page = min(per_page, current_app.config['MAX_PER_PAGE'])
        skip = (page - 1) * per_page
        
        # Create an index on _id for efficient pagination
        mongo.db.songs.create_index([('_id', 1)])
        
        songs = list(mongo.db.songs.find({}, {'ratings': 0}).skip(skip).limit(per_page))
        
        # Convert ObjectId to string for JSON serialization
        for song in songs:
            song['_id'] = str(song['_id'])
            
        return songs
    
    @staticmethod
    def get_average_difficulty(level=None):
        """
        Calculate the average difficulty of songs
        
        Args:
            level (int, optional): Filter songs by level
            
        Returns:
            float: Average difficulty
        """
        match_stage = {}
        if level is not None:
            match_stage = {'level': level}
            
        # Use MongoDB's aggregation for efficient calculation
        pipeline = [
            {'$match': match_stage},
            {'$group': {'_id': None, 'avg_difficulty': {'$avg': '$difficulty'}}}
        ]
        
        result = list(mongo.db.songs.aggregate(pipeline))
        if result:
            return result[0]['avg_difficulty']
        return None
    
    @staticmethod
    def search(message):
        """
        Search songs by artist or title
        
        Args:
            message (str): Search string
            
        Returns:
            list: List of matching songs
        """
        if not message:
            return []
            
        # Create text index for efficient search
        mongo.db.songs.create_index([
            ('artist', 'text'), 
            ('title', 'text')
        ])
        
        # Case-insensitive search using regex
        regex_pattern = {'$regex': message, '$options': 'i'}
        query = {
            '$or': [
                {'artist': regex_pattern},
                {'title': regex_pattern}
            ]
        }
        
        songs = list(mongo.db.songs.find(query, {'ratings': 0}))
        
        # Convert ObjectId to string for JSON serialization
        for song in songs:
            song['_id'] = str(song['_id'])
            
        return songs
    
    @staticmethod
    def add_rating(song_id, rating):
        """
        Add a rating to a song
        
        Args:
            song_id (str): Song ID
            rating (int): Rating value (1-5)
            
        Returns:
            bool: True if rating was added, False otherwise
        """
        try:
            # Validate song_id
            object_id = ObjectId(song_id)
        except:
            return False
            
        # Use $push to add rating to array (creates array if it doesn't exist)
        result = mongo.db.songs.update_one(
            {'_id': object_id},
            {'$push': {'ratings': rating}}
        )
        
        return result.modified_count > 0
    
    @staticmethod
    def get_rating_stats(song_id):
        """
        Get rating statistics for a song
        
        Args:
            song_id (str): Song ID
            
        Returns:
            dict: Rating statistics (average, lowest, highest)
        """
        try:
            # Validate song_id
            object_id = ObjectId(song_id)
        except:
            return None
            
        # Use MongoDB aggregation for efficient statistics calculation
        pipeline = [
            {'$match': {'_id': object_id}},
            {'$project': {
                'avg_rating': {'$avg': '$ratings'},
                'min_rating': {'$min': '$ratings'},
                'max_rating': {'$max': '$ratings'}
            }}
        ]
        
        result = list(mongo.db.songs.aggregate(pipeline))
        if result and 'avg_rating' in result[0]:
            return {
                'average': result[0]['avg_rating'],
                'lowest': result[0]['min_rating'],
                'highest': result[0]['max_rating']
            }
        return None
    
    @staticmethod
    def seed_database():
        """
        Seed the database with data from songs.json
        """
        # Check if collection is already populated
        if mongo.db.songs.count_documents({}) > 0:
            return
            
        try:
            with open('songs.json', 'r') as f:
                songs_data = []
                for line in f:
                    line = line.strip()
                    if line:  # Skip empty lines
                        songs_data.append(json.loads(line))
                        
            if songs_data:
                # Insert songs with empty ratings array
                for song in songs_data:
                    song['ratings'] = []
                mongo.db.songs.insert_many(songs_data)
                
                # Create indexes for common operations
                mongo.db.songs.create_index([('artist', 1)])
                mongo.db.songs.create_index([('title', 1)])
                mongo.db.songs.create_index([('level', 1)])
        except Exception as e:
            print(f"Error seeding database: {e}")
