from flask_restful import Resource, reqparse
from db.members import MemeberFunctions

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
    def post(self):
        try:
            data = Members._members_emails.parse_args()
            Members._members_db.add_emails(**data)
            return {},201
        except Exception as err:
            print(err, type(err))
            return {"message": "An error occurred Adding Emails"}, 500
    
    def put(self):
        try:
            data = Members._members_password.parse_args()
            Members._members_db.update_password(**data)
            return {},200
        except Exception as err:
            print(err, type(err))
            return {"message": "An error occurred updating password."}, 500
    
    def options(self):
        try:
            data = Members._members_admin_privilage.parse_args()
            Members._members_db.toggle_admin_privilage(**data)
            return {},200
        except Exception as err:
            print(err, type(err))
            return {"message": "An error occurred updating privilages."}, 500
