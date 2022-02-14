from flask import request, Blueprint
from db.sessions import SessionFunctions
from util.jwt_functions import authenticate
import traceback 
 
__sessions_db= SessionFunctions()
sessions_apis = Blueprint('sessions_apis', __name__)

@sessions_apis.route('/sessions/expiredSessions', methods=['DELETE'])
@authenticate
def delete_expired_sessions():
    try:
        __sessions_db.delete_expired_sessions()
        return "", 204
    except Exception as err:
        traceback.print_exc()
        print(err, type(err))
        return {"error": "An error occurred Deleting Sessions."}, 500

@sessions_apis.route('/sessions/expiredSessions', methods=['GET'])
@authenticate
def get_expired_sessions():
    try:
        value =__sessions_db.get_expired_sessions()
        return {"data":{"expiredSessions":value}}, 200
    except Exception as err:
        traceback.print_exc()
        print(err, type(err))
        return {"error": "An error occurred Fetching Sessions."}, 500