import csv
import json
import time
import pandas as pd
import sys
import random
from pymongo import MongoClient
from datetime import datetime

def add_csv_to_db(path, layer):
    csvfile = open(path, 'r')
    reader = csv.DictReader(csvfile)
    mongo_client=MongoClient("mongodb+srv://admin:NBtzSCX5fE6CQCdr@globyte-cluster-kxv3b.azure.mongodb.net/globyte?retryWrites=true&w=majority")
    db = mongo_client['globyte']
    col = db['pinpoints']
    for row in reader:
        try:
            parsed_timestamp = row['Date']
            format = '%Y-%m-%d'
            time_values = time.strptime(parsed_timestamp, format)
            timestamp = datetime(time_values[0], time_values[1], time_values[2], time_values[3], time_values[4], time_values[5])
            location = {
                'lat': row['Latitude'],
                'long': row['Longitude']
            }
            magnitude = row['Confirmed']
            if bool(magnitude):
                newEntry = {
                    'timestamp': timestamp,
                    'location': location,
                    'value': magnitude,
                    'layer': layer
                }
                col.insert_one(newEntry)
        except:
            continue


if __name__ == '__main__':
    path = sys.argv[1]
    layer = sys.argv[2]
    add_csv_to_db(path, layer)