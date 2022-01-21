from flask import request, Blueprint, session
from db.members import MemeberFunctions
from util.jwt_functions import generateToken,authenticate
import traceback

user_apis = Blueprint('user_apis', __name__)
_members_db= MemeberFunctions()

@user_apis.route('/users/login', methods=['POST'])
def login():
    requestBody= request.get_json()
    queryParams=request.args
    try:
        result=_members_db.find_flat_by_credentials(requestBody['email'], requestBody['password'])
        token=generateToken(result)
        session['token'] = token
        return {"JWSToken":  token}, 201
    except Exception as err:
        traceback.print_exc()
        return {"error": str(err)},401

@user_apis.route('/users/logout', methods=['DELETE'])
@authenticate
def logout():
        try:
            token = request.headers['Authorization'].replace('Bearer ', '')
            print(token)
            flat_number= _members_db.find_flat_by_token(token)
            _members_db.remove_all_token(flat_number)
            session.pop('token',None)
            return '',204
        except Exception as err:
            traceback.print_exc()
            return {"error": str(err)},500