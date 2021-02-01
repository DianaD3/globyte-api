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
    db = client['globyte'] #alegem baza de date
    hashedPassword = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()) #prima oara face legatura cu serverul meu 
    db.users.insert_one({
        'email': email,
        'username': username,
        'password': hashedPassword,
        'securityAnswer': securityAnswer
    })
    return {'msg': '200 - Successfully registered user!'} #try catch sau Kafka pentru fault tolerance

#checks user credentials and provides a token if they are valid
def login_user(email, password):
    db = client['globyte']
    userFound = db.users.find_one({'email': email}) #primul user gasit in baza de date
    if not bool(userFound):
        return {'err': '401 - Invalid credentials'}
    if bcrypt.checkpw(password.encode('utf-8'), userFound['password']): #parola + partea serverului(salt)-nu e vizibila
        payload = {
            'exp': datetime.datetime.utcnow() + datetime.timedelta(days=5),
            'iat': datetime.datetime.utcnow(),
            'sub': str(userFound['_id'])
        }
        token = jwt.encode(payload, jwt_signature, algorithm='HS256') #criptat cu hs256, nu hashed
        return {'msg': '201 - Authorized', 'token': token.decode('utf-8')} #pune in formatul acela, ii da userului un token
    else:
        return {'err': '401 - Invalid credentials'}

#checks the authorization token every time a request happen
def authorize_user(token):
    if bool(token):
        try:
            payload = jwt.decode(token, jwt_signature, algorithm='HS256') #decripteaza token-ul cu acelasi jwt_signature ca sa extragem payload-ul
        except(jwt.DecodeError, jwt.ExpiredSignatureError):
            return None
        db = client['globyte']
       
        userFound = db.users.find_one({'_id': ObjectId(payload['sub'])}) #obiectul user care are id-ul din payload din db
        return {'msg': '200 - OK', 'user': userFound} if bool(userFound) else {'err': '401 - Access Denied'}
    return None

def change_password(email, newPassword):
    db = client['globyte']
    newHashedPassword = bcrypt.hashpw(newPassword.encode('utf-8'), bcrypt.gensalt())
    #update_one(filtru,actiunea)
    db.users.update_one({'email': email}, {'$set':{'password': newHashedPassword}}) #update poate fie sa stearga $delete,fie sa seteze $set
    return {'msg': '200 - Successfully changed password!'}

def check_answer(email, securityAnswer):
    db = client['globyte']
    print(email)
    print(securityAnswer)
    userFound = db.users.find_one({'email': email, 'securityAnswer': securityAnswer})
    return bool(userFound)
