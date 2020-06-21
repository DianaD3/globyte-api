import requests
import json
import pprint

URL = 'http://localhost:5000'

userToLogIn = {
    'email': 'gica@gmail.com',
    'password': 'ASDqwe123'
}

response = requests.post(url=URL+'/auth/login', data=json.dumps(userToLogIn), headers = {'Content-Type': 'application/json'})

pprint.pprint(json.loads(response.content))