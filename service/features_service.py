from flask import request, Blueprint
from db.features import FeaturesFunctions
from datetime import datetime
from urllib.parse import quote
from util.jwt_functions import authenticate
import traceback 
 
__features_db= FeaturesFunctions()
features_apis = Blueprint('features_apis', __name__)

@features_apis.route('/features', methods=['POST'])
@authenticate
def create_features():
    try:
        data=request.get_json()
        date=datetime.strptime(data['date'].replace("GMT", "+00:00"), "%a, %d %b %Y %H:%M:%S %z")
        focused= data['focused'] if 'focused' in data.keys() else None
        button = quote(data['btn'].encode('utf8')) if 'btn' in data.keys() else None 
        __features_db.add_features(heading=data['heading'],description=data['desc'],image_link=quote(data['img'].encode('utf8')),date=date,focused_word=focused,button_link=button)
        
        return {}, 201
    except ValueError as err:
        traceback.print_exc()
        print(err, type(err))
        return {"error": "Date is not in Javascript UTC format"}, 400
    except Exception as err:
        traceback.print_exc()
        print(err, type(err))
        return {"error": "An error occurred creating Features."}, 500

@features_apis.route('/features', methods=['PUT'])
@authenticate
def edit_features():
    try:
        data=request.get_json()
        date=datetime.strptime(data['date'].replace("GMT", "+00:00"), "%a, %d %b %Y %H:%M:%S %z")
        focused= data['focused'] if 'focused' in data.keys() else None
        button = quote(data['btn'].encode('utf8')) if 'btn' in data.keys() else None 
        __features_db.replace_features(id=data['id'],heading=data['heading'],description=data['desc'],image_link=quote(data['img'].encode('utf8')),date=date,focused_word=focused,button_link=button)
        
        return "", 204
    except ValueError as err:
        traceback.print_exc()
        print(err, type(err))
        return {"error": "Date is not in Javascript UTC format"}, 400
    except Exception as err:
        traceback.print_exc()
        print(err, type(err))
        return {"error": "An error occurred creating Features."}, 500

@features_apis.route('/features', methods=['DELETE'])
@authenticate
def delete_features():
    try:
        data=request.get_json()
        __features_db.delete_feature(id=data['id'])
        return "", 204
    except Exception as err:
        traceback.print_exc()
        print(err, type(err))
        return {"error": "An error occurred Deleting Features."}, 500

@features_apis.route('/features', methods=['GET'])
@authenticate
def get_features():
    try:
        value =__features_db.get_features()
        return {"data":value}, 200
    except Exception as err:
        traceback.print_exc()
        print(err, type(err))
        return {"error": "An error occurred Fetching Features."}, 500