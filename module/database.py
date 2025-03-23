from pymongo import MongoClient

client = MongoClient('mongodb://localhost:27017/')
db = client['moviedatabase']
movie_collection = db['movies_database']
user_collection = db['users_database']
rating_collection = db['movie_rating_collection']