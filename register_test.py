import requests
import json
import pprint

URL = 'http://localhost:5000'

newUser = {
    'username': 'Gica',
    'email': 'gica@gmail.com',
    'password': 'ASDqwe123'
}

response = requests.post(url=URL+'/auth/register', data=json.dumps(newUser), headers = {'Content-Type': 'application/json'})

print(pprint.pprint(json.loads(response.content)))