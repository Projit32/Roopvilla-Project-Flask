from flask.app import Flask
from db.client import MongoDBClient
import bcrypt

class MemeberFunctions:
    _members_collection=MongoDBClient.members_details

    def add_emails(self,flat,emails=[]):
        result=MemeberFunctions._members_collection.update_many({"FLT_NUMS": flat}, {
            "$set" : {
                "EMAILS":emails
            }
        },upsert=True)
        print("Matched: ",result.matched_count)
        print("Modified: ",result.modified_count)

    def update_password(self, flat,password=''):
        hashed=bcrypt.hashpw(bytes(password, 'utf-8'), bcrypt.gensalt(8))
        result=MemeberFunctions._members_collection.update_many({"FLT_NUMS":flat}, {
            "$set" : {
                "ACCESS_KEY":hashed.decode("utf-8")
            }
        },upsert=True)
        print("Matched: ",result.matched_count)
        print("Modified: ",result.modified_count)
    
    def toggle_admin_privilage(self, flat, admin_privilages=False):
        result=MemeberFunctions._members_collection.update_one({"FLT_NUMS":flat}, {
            "$set" : {
                "ADMIN_ACCESS":admin_privilages
            }
        },upsert=True)
        print("Matched: ",result.matched_count)
        print("Modified: ",result.modified_count)
