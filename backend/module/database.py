from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv()

MONGODB_DATABASE_NAME = os.getenv('MONGODB_DATABASE_NAME')
MOVIE_COLLECTION_NAME = os.getenv('MOVIE_COLLECTION_NAME')
USERS_COLLECTION_NAME = os.getenv('USERS_COLLECTION_NAME')
RATING_COLLECTION_NAME = os.getenv('RATING_COLLECTION_NAME')
MONGODB_HOST_NAME = os.getenv('MONGODB_HOST_NAME')

#client = MongoClient('mongodb://user:password@localhost:27017/')
client = MongoClient(f'mongodb://{MONGODB_HOST_NAME}:27017/')
db = client[MONGODB_DATABASE_NAME]
movie_collection = db[MOVIE_COLLECTION_NAME]
user_collection = db[USERS_COLLECTION_NAME]
rating_collection = db[RATING_COLLECTION_NAME]