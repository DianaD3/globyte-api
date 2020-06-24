import bcrypt
from pymongo import MongoClient # connection
import json # json
client = MongoClient(json.load(open('./config.json'))['endpoint'])
import jwt
import datetime
from bson.objectid import ObjectId

jwt_signature = json.load(open('./config.json'))['jwt_signature']

# checks email to be unique and valid
def is_valid_email(email):
    db = client['globyte']
    userFound = db.users.find_one({'email': email})
    return not bool(userFound) #if there is another user with this email, then this email is not valid


#adds a new user to the database
def register_new_user(username, email, password, securityAnswer):
    db = client['globyte']
    hashedPassword = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    db.users.insert_one({
        'email': email,
        'username': username,
        'password': hashedPassword,
        'securityAnswer': securityAnswer
    })
    return {'msg': '200 - Successfully registered user!'}

#checks user credentials and provides a token if they are valid
def login_user(email, password):
    db = client['globyte']
    userFound = db.users.find_one({'email': email})
    if not bool(userFound):
        return {'err': '401 - Invalid credentials'}
    if bcrypt.checkpw(password.encode('utf-8'), userFound['password']):
        payload = {
            'exp': datetime.datetime.utcnow() + datetime.timedelta(days=5),
            'iat': datetime.datetime.utcnow(),
            'sub': str(userFound['_id'])
        }
        token = jwt.encode(payload, jwt_signature, algorithm='HS256')
        return {'msg': '201 - Authorized', 'token': token.decode('utf-8')}
    else:
        return {'err': '401 - Invalid credentials'}

#checks the authorization token 
def authorize_user(token):
    if bool(token):
        try:
            payload = jwt.decode(token, jwt_signature, algorithm='HS256')
        except(jwt.DecodeError, jwt.ExpiredSignatureError):
            return None
        db = client['globyte']
        print(payload)
        userFound = db.users.find_one({'_id': ObjectId(payload['sub'])})
        print(userFound)
        return {'msg': '200 - OK', 'user': userFound} if bool(userFound) else {'err': '401 - Access Denied'}
    return None

def change_password(email, newPassword):
    db = client['globyte']
    newHashedPassword = bcrypt.hashpw(newPassword.encode('utf-8'), bcrypt.gensalt())
    db.users.update_one({'email': email}, {'$set':{'password': newHashedPassword}})
    return {'msg': '200 - Successfully changed password!'}

def check_answer(email, securityAnswer):
    db = client['globyte']
    print(email)
    print(securityAnswer)
    userFound = db.users.find_one({'email': email, 'securityAnswer': securityAnswer})
    return bool(userFound)
