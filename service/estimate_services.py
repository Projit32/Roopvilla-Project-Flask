from flask import request, Blueprint
from db.estimates import EstimatesFunctions
from datetime import datetime
from util.jwt_functions import authenticate
import traceback 
 
__estimates_db= EstimatesFunctions()
estimates_apis = Blueprint('estimates_apis', __name__)

@estimates_apis.route('/estimates', methods=['POST'])
@authenticate
def create_estimates():
    try:
        data=request.get_json()
        __estimates_db.add_estimates(name=data['name'], monthly=data['monthly'],annually=data['annually'])
        return {}, 201
    except Exception as err:
        traceback.print_exc()
        print(err, type(err))
        return {"error": "An error occurred creating Estimates."}, 500

@estimates_apis.route('/estimates', methods=['PATCH'])
@authenticate
def edit_estimates():
    try:
        data=request.get_json()
        __estimates_db.edit_estimates(id=data['id'],name=data['name'], monthly=data['monthly'],annually=data['annually'])
     
        return "", 204
    except Exception as err:
        traceback.print_exc()
        print(err, type(err))
        return {"error": "An error occurred creating Estimates."}, 500

@estimates_apis.route('/estimates', methods=['DELETE'])
@authenticate
def delete_estimates():
    try:
        data=request.get_json()
        __estimates_db.delete_estimates(id=data['id'])
        return "", 204
    except Exception as err:
        traceback.print_exc()
        print(err, type(err))
        return {"error": "An error occurred Deleting Estimate."}, 500

@estimates_apis.route('/estimates', methods=['GET'])
@authenticate
def get_estimates():
    try:
        value =__estimates_db.get_estimates()
        return {"data":value}, 200
    except Exception as err:
        traceback.print_exc()
        print(err, type(err))
        return {"error": "An error occurred Fetching Estimate."}, 500