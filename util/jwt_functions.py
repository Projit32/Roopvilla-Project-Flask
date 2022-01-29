import os
import jwt
import datetime
import functools
import json
from flask import request, session
from db.members import MemeberFunctions
from werkzeug.datastructures import ImmutableMultiDict
from db.members import MemeberFunctions

_members_db= MemeberFunctions()

def generateToken(flatNumber):
    payload = {
                'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1),
                'iat': datetime.datetime.utcnow(),
                "flat": flatNumber
            }
    token=jwt.encode(payload, os.getenv('JWT_SECRET'), algorithm="HS256")
    MemeberFunctions().add_token(flat=flatNumber, token=token)
    return token



def authenticate(func):
    @functools.wraps(func)
    def decodeToken(*args, **kwargs):
        try:
            token = 'token'
            if token in session.keys():
                token = session['token']
                print("From Session")
            else:
                token = request.headers['Authorization'].replace('Bearer ', '')
                print("From Headers")
            decode =jwt.decode(token, os.getenv('JWT_SECRET'), algorithms=["HS256"])
            http_args = request.args.to_dict()
            http_args ['ADM_NAME'] = _members_db.find_owner_by_token(token)
            request.args = ImmutableMultiDict(http_args)
            return func(*args, **kwargs)
        except jwt.ExpiredSignatureError:
            return {"error":"Token Expired"}, 401
        except KeyError as err:
            return {"error":"Missing Authorization"}, 401
    return decodeToken
