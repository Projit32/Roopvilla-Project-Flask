from audioop import add
from flask_restful import Resource, reqparse
from flask import request
from db.members import MemeberFunctions
from util.jwt_functions import authenticate
import traceback

class Members(Resource):
    _members_db= MemeberFunctions()
    _members_emails  = reqparse.RequestParser()
    _members_emails.add_argument('flat',
                            type=str,
                            required=True,
                            help="Need a Flat Number to update the emails"
                            )
    _members_emails.add_argument('emails',
                            type=str,
                            required=True,
                            action='append',
                            help="Must be an array of valid emails"
                            )
    _members_password = reqparse.RequestParser()
    _members_password.add_argument('flat',
                            type=str,
                            required=True,
                            help="Need a Flat Number to update the password"
                            )
    _members_password.add_argument('password',
                            type=str,
                            required=True,
                            help="A strong password of choice is needed"
                            )
    _members_admin_privilage=reqparse.RequestParser()
    _members_admin_privilage.add_argument('flat',
                            type=str,
                            required=True,
                            help="Need a Flat Number to update the password"
                            )
    _members_admin_privilage.add_argument('admin_privilages',
                            default=False,
                            type=bool,
                            required=False,
                            help="Privilage to be set for that Flat Number"
                            )
    def patch(self):
        @authenticate
        def add_emails():
            try:
                data = Members._members_emails.parse_args()
                Members._members_db.add_emails(**data)
                return {},201
            except Exception as err:
                traceback.print_exc()
                print(err, type(err))
                return {"message": "An error occurred Adding Emails"}, 500
        return add_emails()
    
    def put(self):
        @authenticate
        def update_password():
            try:
                data = Members._members_password.parse_args()
                Members._members_db.update_password(**data)
                return {},200
            except Exception as err:
                traceback.print_exc()
                print(err, type(err))
                return {"message": "An error occurred updating password."}, 500
        return update_password()
    
    def options(self):
        @authenticate
        def toggle_admin():
            try:
                data = Members._members_admin_privilage.parse_args()
                Members._members_db.toggle_admin_privilage(**data)
                return {},200
            except Exception as err:
                traceback.print_exc()
                print(err, type(err))
                return {"message": "An error occurred updating privilages."}, 500
        return toggle_admin()
    
    def post(self):
        @authenticate
        def add_member():
            try:
                data = request.get_json()
                Members._members_db.add_members(name=data['name'],emails=data['emails'],flats=data['flats'])
                return {},201
            except Exception as err:
                traceback.print_exc()
                print(err, type(err))
                return {"message": "An error occurred adding member."}, 500
        return add_member()

    def delete(self):
        @authenticate
        def remove_member():
            try:
                data = request.get_json()
                complete_removal=request.args.get('complete') == 'Y'
                print("complete removal",complete_removal, type(complete_removal))
                if(complete_removal):
                    Members._members_db.remove_members(email=data['email'])
                else:
                    Members._members_db.remove_flat_ownership(flat=data['flat'])

                return {},204
            except Exception as err:
                traceback.print_exc()
                print(err, type(err))
                return {"message": "An error occurred removing member."}, 500
        return remove_member()
    
    def get(self):
        @authenticate
        def get_all_flats():
            try:
                data=Members._members_db.get_all_flats()
                return {"flats":data},200
            except Exception as err:
                traceback.print_exc()
                print(err, type(err))
                return {"message": "An error occurred getting all flats."}, 500
        return get_all_flats()
