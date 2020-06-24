from pymongo import MongoClient # connection
import json # json

# create the mongo client
client = MongoClient(json.load(open("./config.json"))['endpoint'])

# function to drop all pinpoints
def drop_collection():
    # connect to db
    db = client['globyte']
    # drop collection
    db.drop_collection('pinpoints')

    # operation was completed
    return True