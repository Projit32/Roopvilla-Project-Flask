from flask import request, Blueprint
from db.ef import EmergencyFundFunctions
from util.jwt_functions import authenticate
import traceback 
 
_ef_db= EmergencyFundFunctions()
ef_apis = Blueprint('ef_apis', __name__)

@ef_apis.route('/emergencyFunds/initialize', methods=['POST'])
@authenticate
def create_ef():
    try:
        result = _ef_db.ef_initialization()
        return {"Created":"YES"}, 201
    except Exception as err:
        traceback.print_exc()
        print(err, type(err))
        return {"error": "An error occurred creating EF."}, 500

@ef_apis.route('/emergencyFunds/updateRate', methods=['PATCH'])
@authenticate
def update_ef():
    try:
        data= request.get_json()
        _ef_db.ef_update_flat_rate(flat_number=data['flat_number'], rate=float(data['rate']))
        return {"Updated": "YES"}, 200
    except Exception as err:
        traceback.print_exc()
        print(err, type(err))
        return {"error": "An error occurred updating EF."}, 500

@ef_apis.route('/emergencyFunds/getFlatRates', methods=['GET'])
@authenticate
def get_ef_rates():
    try:
        data=_ef_db.get_ef_details()
        return {"data": data}, 200
    except Exception as err:
        traceback.print_exc()
        print(err, type(err))
        return {"error": "An error occurred getting EF."}, 500