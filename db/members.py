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
    

    def find_flat_by_credentials(self, username, password):
        user = MemeberFunctions._members_collection.find_one({"EMAILS":username, "ADMIN_ACCESS":True})
        if(user is None):
            raise Exception("Username/Password is incorrect")
        access_key =user["ACCESS_KEY"]
        if(bcrypt.checkpw(bytes(password, 'utf-8'),bytes(access_key, 'utf-8'))):
            return user['FLT_NUMS']
        else:
            raise Exception("Username/Password is incorrect")
    
    def remove_all_token(self, flatNumber):
        result = MemeberFunctions._members_collection.update_one({"FLT_NUMS": {"$in":flatNumber}},{
            "$set":{
                "ADM_TOKENS": []
            }
        })
        print("Matched: ",result.matched_count)
        print("Modified: ",result.modified_count)
    
    def find_flat_by_token(self, token):
        user=MemeberFunctions._members_collection.find_one({"ADM_TOKENS":token})
        print("type",type(user), "value", user)
        if(user is not None):
            return user['FLT_NUMS']
        else:
            raise Exception("Token Not found")

    
    def add_token(self, flat, token):
        print(flat, token)
        result=MemeberFunctions._members_collection.update_one({"FLT_NUMS": {"$in":flat}}, {
            "$push" : {
                "ADM_TOKENS":token
            }
        },upsert=True)
        print("Matched: ",result.matched_count)
        print("Modified: ",result.modified_count)