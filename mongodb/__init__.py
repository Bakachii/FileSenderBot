import os
from pymongo import MongoClient
from main import DB_URL

client = MongoClient(DB_URL)
db = client['mydatabase']
users_collection = db['users']
protect_value = db['protect_content']
channel_button_value = db['channel_button']

protect_value.update_one({}, {"$setOnInsert": {"protect_content": False}}, upsert=True)
channel_button_value.update_one({}, {"$setOnInsert": {"channel_button": False}}, upsert=True)


def start():
    return db

BASE = db
SESSION = start()
