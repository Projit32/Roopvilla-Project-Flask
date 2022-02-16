from flask import request, Blueprint
from db.flats import FlatsFunctions
from util.api_exceptions import RequestException
from util.jwt_functions import authenticate
import traceback 
 
__flats_db= FlatsFunctions()
flats_apis = Blueprint('flats_apis', __name__)

@flats_apis.route('/flats/unoccupiedFlats', methods=['GET'])
@authenticate
def get_expired_sessions():
    try:
        value =__flats_db.get_unoccupied_flats()
        return {"data":{"unoccupiedFlats":value}}, 200
    except RequestException as err:
        traceback.print_exc()
        print(err, type(err))
        return {"error": str(err)}, 400
    except Exception as err:
        traceback.print_exc()
        print(err, type(err))
        return {"error": "An error occurred Fetching Sessions."}, 500