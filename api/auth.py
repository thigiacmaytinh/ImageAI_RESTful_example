from django.conf import settings
import jwt,json

def decode(token):
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms='HS256')
        return True
    except jwt.ExpiredSignatureError:
        return False

def getInformationFromToken(token):
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms='HS256')
        return payload
    except jwt.ExpiredSignatureError:
        return None
    except:
        return None

def encode(payload):
    jwt_token = {'token': jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256').decode('utf-8')}
    return jwt_token