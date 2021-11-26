from flask.globals import request
from flask_restful import Resource, reqparse
from db.members import MemeberFunctions
from util.jwt_functions import generateToken,authenticate
import traceback

class Users(Resource):
    _members_db= MemeberFunctions()

    def post(self):
        requestBody= request.get_json()
        queryParams=request.args
        try:
            result=Users._members_db.find_flat_by_credentials(requestBody['email'], requestBody['password'])
            return {"JWSToken": generateToken(result) }, 201
        except Exception as err:
            traceback.print_exc()
            return {"error": str(err)},401
    
    def delete(self):
        @authenticate
        def logout():
            try:
                token = request.headers['Authorization'].replace('Bearer ', '')
                print(token)
                flat_number= Users._members_db.find_flat_by_token(token)
                Users._members_db.remove_all_token(flat_number)
                return None,204
            except Exception as err:
                traceback.print_exc()
                return {"error": str(err)},500
        return logout()