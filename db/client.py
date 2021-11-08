import os
from pymongo import MongoClient

MongoDBClient = MongoClient(os.getenv('MONGO_DB')).roopvilla_maintenance