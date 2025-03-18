# filepath: d:\movie_recommendation_system\database\db.py
import os
import pymongo

class MovieDatabase:
    def __init__(self):
        mongo_uri = os.environ.get("MONGO_URI", "mongodb://localhost:27017")
        self.client = pymongo.MongoClient(mongo_uri)
        self.db = self.client["movie_recommendation_db"]
        self.movies = self.db["movies"]
        self.similarities = self.db["similarities"]
    
    def get_movie_by_title(self, title):
        return self.movies.find_one({"title": title})
    
    def get_similarity_matrix(self):
        # Retrieve pre-computed similarity matrix
        return self.similarities.find_one({"type": "movie_similarities"})["matrix"]