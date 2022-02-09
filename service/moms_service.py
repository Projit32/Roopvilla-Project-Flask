from flask import request, Blueprint
from db.moms import MinutesOfMeetingFunctions
from datetime import datetime
import html
from util.api_exceptions import RequestException
from util.jwt_functions import authenticate
import traceback 
 
__moms_db= MinutesOfMeetingFunctions()
moms_apis = Blueprint('moms_apis', __name__)

@moms_apis.route('/moms', methods=['POST'])
@authenticate
def create_mom():
    try:
        data=request.get_json()
        date=datetime.strptime(data['date'].replace("GMT", "+00:00"), "%a, %d %b %Y %H:%M:%S %z")
        
        moms_data=list()
        for item in data['moms']:
            moms_data.append({
                "TOPIC":html.escape(item['topic']),
                "DECISION":html.escape(item['decision'])
            })
        
        __moms_db.insert_mom(date=date,moms=moms_data)
        return {}, 201
    except RequestException as err:
        traceback.print_exc()
        print(err, type(err))
        return {"error": str(err)}, 400
    except ValueError as err:
        traceback.print_exc()
        print(err, type(err))
        return {"error": "Date is not in Javascript UTC format"}, 400
    except Exception as err:
        traceback.print_exc()
        print(err, type(err))
        return {"error": "An error occurred creating MOM Record."}, 500

@moms_apis.route('/moms', methods=['DELETE'])
@authenticate
def delete_mom():
    try:
        data=request.get_json()
        date=datetime.strptime(data['date'].replace("GMT", "+00:00"), "%a, %d %b %Y %H:%M:%S %z")
        __moms_db.delete_mom(date=date)
        return "", 204

    except ValueError as err:
        traceback.print_exc()
        print(err, type(err))
        return {"error": "Date is not in Javascript UTC format"}, 400
    except Exception as err:
        traceback.print_exc()
        print(err, type(err))
        return {"error": "An error occurred Deleting MOM Record."}, 500

@moms_apis.route('/moms', methods=['GET'])
@authenticate
def get_moms():
    try:
        data=queryParams=request.args
        start=datetime.strptime(data.get('startDate').replace("GMT", "+00:00"), "%a, %d %b %Y %H:%M:%S %z")
        end=datetime.strptime(data.get('endDate').replace("GMT", "+00:00"), "%a, %d %b %Y %H:%M:%S %z")
        if start>end:
            raise RequestException("Start date cannot be later than end date!")
        
        value = __moms_db.get_mom(start=start, end=end)
        return {"data":value}, 200

    except RequestException as err:
        traceback.print_exc()
        print(err, type(err))
        return {"error": str(err)}, 400    
    except ValueError as err:
        traceback.print_exc()
        print(err, type(err))
        return {"error": "Date is not in Javascript UTC format"}, 400
    except Exception as err:
        traceback.print_exc()
        print(err, type(err))
        return {"error": "An error occurred Fetching MOM Record."}, 500