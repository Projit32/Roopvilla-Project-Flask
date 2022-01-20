from flask import request, Blueprint, jsonify
from db.members import MemeberFunctions
from util.jwt_functions import authenticate
import traceback

_members_db= MemeberFunctions()
member_apis = Blueprint('member_apis', __name__)

@member_apis.route('/members/setEmails', methods=['PUT'])
@authenticate
def set_emails():
    try:
        data =request.get_json()
        _members_db.add_emails(flat=data['flat'], emails=data['emails'])
        return '',204
    except Exception as err:
        traceback.print_exc()
        print(err, type(err))
        return {"message": "An error occurred Adding Emails"}, 500

@member_apis.route('/members/changePassword', methods=['PATCH'])
@authenticate
def update_password():
    try:
        data = request.get_json()
        _members_db.update_password(flat=data['flat'],password=data['password'])
        return '',204
    except Exception as err:
        traceback.print_exc()
        print(err, type(err))
        return {"message": "An error occurred updating password."}, 500

@member_apis.route('/members/changeAdminPrivilages', methods=['OPTIONS'])
@authenticate
def toggle_admin():
    try:
        data = request.get_json()
        privilage=data['admin_privilages']
        print('privilage req:', privilage, "Type: ", type(privilage))
        _members_db.toggle_admin_privilage(flat=data['flat'], admin_privilages=privilage)
        return '',204
    except Exception as err:
        traceback.print_exc()
        print(err, type(err))
        return {"message": "An error occurred updating privilages."}, 500

@member_apis.route('/members', methods=['POST'])
@authenticate
def add_member():
    try:
        data = request.get_json()
        _members_db.add_members(name=data['name'],emails=data['emails'],flats=data['flats'])
        return {},201
    except Exception as err:
        traceback.print_exc()
        print(err, type(err))
        return {"message": "An error occurred adding member."}, 500


@member_apis.route('/members', methods=['DELETE'])
@authenticate
def remove_member():
    try:
        data = request.get_json()
        complete_removal=request.args.get('complete') == 'Y'
        print("complete removal",complete_removal, type(complete_removal))
        if(complete_removal):
            _members_db.remove_members(email=data['email'])
        else:
            _members_db.remove_flat_ownership(flat=data['flat'],email=data['email'])

        return '',204
    except Exception as err:
        traceback.print_exc()
        print(err, type(err))
        return {"message": "An error occurred removing member."}, 500


@member_apis.route('/members', methods=['GET'])
@authenticate
def get_all_members():
    try:
        data=_members_db.get_all_members()
        return {"data":data},200
    except Exception as err:
        traceback.print_exc()
        print(err, type(err))
        return {"message": "An error occurred getting all flats."}, 500

