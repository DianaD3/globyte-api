from pymongo import MongoClient # connection
from datetime import datetime # time
import json # json

# create the mongo client
client = MongoClient(json.load(open('./config.json'))['endpoint'])

# function for inserting a single data point
def insert_data_point(latitude, longitude, value, layer, timestamp=None):
    # connect to a database
    db = client['globyte']
    # select a table (if non existent it will automatically create one)
    col = db['pinpoints']
    # check if we have a valid timestamp (use prepare_time to get a formatted value)
    if timestamp == None:
        timestamp = str(datetime.today()).split('.')[0]
    # prepare the data for insertion
    data = {
        'timestamp': timestamp,
        'location': {
            'lat': latitude,
            'long': longitude
        },
        'value': value,
        'layer': layer
    }
    # insert the data
    col.insert_one(data)

    # operation was completed
    return True

def insert_many_points(points):
    # connect to a database
    db = client['globyte']
    # select a table (if non existent it will automatically create one)
    col = db['pinpoints']
    # insert the data
    col.insert_many(points)

    # operation was completed
    return True