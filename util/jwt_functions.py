import os
import jwt
import datetime
import functools
import json
from flask import request
from db.members import MemeberFunctions


def generateToken(flatNumber):
    payload = {
                'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1),
                'iat': datetime.datetime.utcnow(),
                "flat": flatNumber
            }
    token=jwt.encode(payload, os.getenv('JWT_SECRET'), algorithm="HS256")
    MemeberFunctions().add_token(flat=flatNumber, token=token)
    print(token)
    return token



def authenticate(func):
    @functools.wraps(func)
    def decodeToken(*args, **kwargs):
        try:
            token = request.headers['Authorization'].replace('Bearer ', '')
            decode =jwt.decode(token, os.getenv('JWT_SECRET'), algorithms=["HS256"])
            return func(*args, **kwargs)
        except jwt.ExpiredSignatureError:
            return {"error":"Token Expired"}, 401
        except KeyError as err:
            return {"error":"Missing Authorization"}, 401
    return decodeToken
