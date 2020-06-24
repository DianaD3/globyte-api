from flask import Flask # Flask
from flask import request
from flask_cors import CORS
from Globyte import get, prepare, insert # our functions
from Globyte import auth
import numpy as np

app = Flask(__name__) # init flask
CORS(app, allow_headers='*')

@app.route('/') # home route
def index():
    return "Globyte"

@app.route('/get/collection') # get pinpoint collection
def get_collections():
    return prepare.data_to_json(get.get_collection())

@app.route('/get/layer/<layer_name>') # get single layer
def get_layer(layer_name):
    return prepare.data_to_json(get.get_layer(str(layer_name)))

@app.route('/get/layer/location/<layer_name>/<latmin>/<latmax>/<longmin>/<longmax>') # get specific location pinpoints from layer
def get_layer_by_location(layer_name,latmin,latmax,longmin,longmax):
    return prepare.data_to_json(get.get_layer_by_location(str(layer_name),float(latmin),float(latmax),float(longmin),float(longmax)))

@app.route('/get/layer/time/<layer_name>/<datestart>/<timestart>/<datestop>/<timestop>') # get specific time pinpoint from layer
def get_layer_by_time(layer_name, datestart, timestart, datestop, timestop):
    start = datestart + " " + timestart
    stop = datestop + " " + timestop
    print("Giving data to the client!")
    print(start)
    print(stop)
    print(layer_name)
    json_data = get.get_layer_by_timestamp(str(layer_name),str(start),str(stop))
    geojson =  {
        'type': 'FeatureCollection',
        'features': list()
    }
    for point in json_data['pinpoints']:
        geojson['features'].append(prepare.json_to_geojson(point))
    return prepare.data_to_json(geojson)

@app.route('/get/layers')
def get_layers():
    data = get.layers()
    authorized = False
    headers = request.headers
    if bool(headers['Authorization']):
        response = auth.authorize_user(headers['Authorization'] if 'Authorization' in headers else None)
        if bool(response):
            authorized = True
    
    if not authorized and 'Volcanic' in data:
        data = ['Volcanic']
    return prepare.data_to_json({'msg': '200 - OK', 'layers': data})

@app.route('/insert/single', methods=['POST'])
def insert_single():
    data = request.get_json()
    if insert.insert_data_point(data['location']['lat'],data['location']['long'],data['value'],data['layer'],data['timestamp']):
    	return 'Inserted'
    return 'Error'

@app.route('/insert/multiple', methods=['POST'])
def insert_multiple():
    data = request.get_json()
    insert_data = []
    for row in data['pinpoints']:
        insert_data = prepare.prepare_points(insert_data, row['location']['lat'], row['location']['long'], row['value'], row['layer'],row['timestamp'])
    if insert.insert_many_points(insert_data):
        return 'Insert'
    else:
        return 'Error'

@app.route('/ml/forecasting', methods=["POST"])
def forecasting():
    data = request.get_json()['input']
    output = ml.forecast(data, int(0.1*len(data)))
    return prepare.data_to_json({
        'output': output
    })

@app.route('/ml/anomaly', methods=["POST"])
def anomaly():
    data = request.get_json()['input']
    output = ml.anomaly_detection(data).tolist()
    return prepare.data_to_json({
        'output': output
    })

@app.route('/auth/login', methods=["POST"])
def login():
    data = request.get_json()
    if not ('email' in data and 'password' in data):
        return prepare.data_to_json({
            'err': '400 - Bad request'
        })

    email = data['email']
    password = data['password']

    response = auth.login_user(email, password)

    return prepare.data_to_json(response)



@app.route('/auth/register', methods=["POST"])
def register():
    data = request.get_json(force=True)
    # basic validation
    if not ('username' in data and 'email' in data and 'password' in data and 'securityAnswer' in data and auth.is_valid_email(data['email'])):
        print('Bad credentials')
        return prepare.data_to_json({
            'err': '400 - Bad request'
        })
    username = data['username']
    email = data['email']
    password = data['password']
    securityAnswer = data['securityAnswer']

    response = auth.register_new_user(username, email, password, securityAnswer)

    return prepare.data_to_json(response)

@app.route('/auth/getCurrentUser', methods=["POST"])
def get_current_user():
    print(request.headers)
    headers = request.headers
    if bool(headers['Authorization']):
        response = auth.authorize_user(headers['Authorization'])
        print(response)
        return prepare.data_to_json(response)
    else:
        return prepare.data_to_json({
            'err': '401 - Access Denied'
        })

@app.route('/auth/changePassword', methods=["POST"])
def change_password():
    data = request.get_json(force=True)
    if not ('email' in data and 'newPassword' in data and 'securityAnswer' in data):
        return prepare.data_to_json({
            'err': '400 - Bad request'
        })
    
    email = data['email']
    newPassword = data['newPassword']
    securityAnswer = data['securityAnswer']
    
    isAnswerOk = auth.check_answer(email, securityAnswer)
    
    if isAnswerOk:
        response = auth.change_password(email, newPassword)
        return response;
    else:
        return prepare.data_to_json({
            'err': '401 - Access Denied'
        })

# run the app
if __name__ == "__main__":
    app.run(host="0.0.0.0")
