from pymongo import MongoClient # connection
import json # json
from datetime import datetime
#from . import data_generator as generator
# create client
client = MongoClient(json.load(open('./config.json'))['endpoint'])
#client = generator.generate_new()
# function to visualize a single collection from a database

def layers():
    db = client['globyte']
    layersFound = db.pinpoints.distinct('layer')
    return layersFound

def get_collection():
    print("Safe here")
    # create return dict
    return_dict = {
        'pinpoints': list()
    }
    print(client)
    print("#######################")
    db = client['globyte']
    print(db)
    print("#######################")
    col = db.pinpoints.find()
    print(col)
    print("#######################")
    # print all the contents inside the collection
    for data in col:
        return_dict['pinpoints'].append(data)
    print(return_dict)
    return return_dict
    
# function to visualize a single layer from a database
def get_layer(layer_name):
    # create return dict
    return_dict = {
        'pinpoints': list()
    }
    db = client['globyte']
    col = db['pinpoints']
    # print all the contents inside the collection
    for data in col:
        if data['layer'] == layer_name:
            return_dict['pinpoints'].append(data)
    return return_dict

# function to visualize a single layer that is placed in the latmin-latmax and longmin-longmax range
def get_layer_by_location(layer_name, latmin, latmax, longmin, longmax):
    # create return dict
    return_dict = {
        'pinpoints': list()
    }
    db = client['globyte']
    col = db['pinpoints']
    # print all the contents inside the collection
    for data in col:
        # check for a specific layer
        if data['layer'] == layer_name:
            # search all pinpoints in the latmin-latmax and longmin-longmax range
            if data['location']['lat'] >= latmin and data['location']['lat'] <= latmax:
                if data['location']['long'] >= longmin and data['location']['long'] <= longmax:
                    return_dict['pinpoints'].append(data)

    # return all the pinpoints
    return return_dict

# function to visualize a single layer that is placed in the timestart-timestop range
def get_layer_by_timestamp(layer_name,timestart,timestop):
    # create return dict
    return_dict = {
        'pinpoints': list()
    }
    db = client['globyte']
    col = db.pinpoints.find({'layer': layer_name})
    # print all the contents inside the collection
    for data in col:
        if datetime.strptime(str(data['timestamp']),'%Y-%m-%d %H:%M:%S') >= datetime.strptime(timestart,'%Y-%m-%d %H:%M:%S') and datetime.strptime(str(data['timestamp']),'%Y-%m-%d %H:%M:%S') <= datetime.strptime(timestop,'%Y-%m-%d %H:%M:%S'):
            return_dict['pinpoints'].append(data)
    return return_dict