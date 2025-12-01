from pymongo import MongoClient
from datetime import datetime

def get_mongo_client(host, port, user, password, auth_db):
    uri = f"mongodb://{user}:{password}@{host}:{port}/?authSource={auth_db}"
    client = MongoClient(uri)
    return client

def get_collection(client, db_name, collection_name):
    return client[db_name][collection_name]

def flat_exists(collection, flat_id):
    return collection.find_one({"id": flat_id}) is not None

def insert_flat(collection, flat):
    flat["first_seen"] = datetime.utcnow()
    collection.insert_one(flat)
