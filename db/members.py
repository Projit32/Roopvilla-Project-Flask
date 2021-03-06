from db.client import MongoDBClient
from db.ef import EmergencyFundFunctions
from db.flats import FlatsFunctions
import bcrypt
from util.api_exceptions import RequestException

class MemeberFunctions:
    __members_collection=MongoDBClient.members_details
    __flats_db=FlatsFunctions()
    __ef_db= EmergencyFundFunctions()

    def add_emails(self,flat,emails=[]):
        result=self.__members_collection.update_many({"FLT_NUMS": flat}, {
            "$set" : {
                "EMAILS":emails
            }
        },upsert=True)
        print("Matched: ",result.matched_count)
        print("Modified: ",result.modified_count)

    def update_password(self, flat,password=''):
        hashed=bcrypt.hashpw(bytes(password, 'utf-8'), bcrypt.gensalt(8))
        result=self.__members_collection.update_many({"FLT_NUMS":flat}, {
            "$set" : {
                "ACCESS_KEY":hashed.decode("utf-8")
            }
        },upsert=True)
        print("Matched: ",result.matched_count)
        print("Modified: ",result.modified_count)
    
    def toggle_admin_privilage(self, flat, admin_privilages=False):
        result=self.__members_collection.update_one({"FLT_NUMS":flat}, {
            "$set" : {
                "ADMIN_ACCESS":admin_privilages
            }
        },upsert=True)
        print("Matched: ",result.matched_count)
        print("Modified: ",result.modified_count)
    

    def find_flat_by_credentials(self, username, password):
        user = self.__members_collection.find_one({"EMAILS":username, "ADMIN_ACCESS":True})
        if(user is None):
            raise Exception("Username/Password is incorrect")
        access_key =user["ACCESS_KEY"]
        if(bcrypt.checkpw(bytes(password, 'utf-8'),bytes(access_key, 'utf-8'))):
            return user['FLT_NUMS']
        else:
            raise Exception("Username/Password is incorrect")
    
    def remove_all_token(self, flatNumber):
        result = self.__members_collection.update_one({"FLT_NUMS": {"$in":flatNumber}},{
            "$set":{
                "ADM_TOKENS": []
            }
        })
        print("Matched: ",result.matched_count)
        print("Modified: ",result.modified_count)
    
    def find_flat_by_token(self, token):
        user=self.__members_collection.find_one({"ADM_TOKENS":token})
        if(user is not None):
            return user['FLT_NUMS']
        else:
            raise Exception("Token Not found")
    
    def find_owner_by_token(self, token):
        user=self.__members_collection.find_one({"ADM_TOKENS":token})
        if(user is not None):
            return user['OWNER_NAME']
        else:
            raise Exception("Token Not found")

    
    def add_token(self, flat, token):
        print(flat, token)
        result=self.__members_collection.update_one({"FLT_NUMS": {"$in":flat}}, {
            "$push" : {
                "ADM_TOKENS":token
            }
        },upsert=True)
        print("Matched: ",result.matched_count)
        print("Modified: ",result.modified_count)
    
    def add_members(self ,name,emails=[], flats=[]):
        for flat in flats:
            if  self.__flats_db.get_occupied_status(flat):
                raise RequestException("Flat "+flat+" is Already occupied!")
        
        result=self.__members_collection.insert_one({
            "OWNER_NAME":name,
            "QNT": len(flats),
            "EMAILS":emails,
            "FLT_NUMS": flats,
            "ACCESS_KEY":"",
            "TOKENS":[],
            "ADMIN_ACCESS":False
        })
        print("New Inserted Acknowledged : ",result.acknowledged)
        for flat in flats:
            self.__ef_db.ef_update_flat_rate(flat_number=flat, rate=0.1)
            self.__flats_db.change_occupied_status(flat=flat,status=True)
    
    def remove_members(self ,email):
        user=self.__members_collection.find_one({
             "EMAILS": email
        })
        if(user is None):
            raise Exception("User Not found")

        for flat in user["FLT_NUMS"]:
            self.__ef_db.ef_update_flat_rate(flat_number=flat, rate=0.0)
            self.__flats_db.change_occupied_status(flat=flat,status=False)

        result=self.__members_collection.delete_one({
            "EMAILS": email
        })
        print("Delete Acknowledged : ",result.acknowledged)
    
    def remove_flat_ownership(self,flat,email):
        member=self.__members_collection.find_one({
                 "EMAILS": email
        })
        if(member is not None):
            flats= member['FLT_NUMS']
        else:
            raise Exception("Member Not found")
        
        flats.remove(flat)

        result=self.__members_collection.update_one({"OWNER_NAME":member['OWNER_NAME']},{
            "$set":{
                 "FLT_NUMS": flats
            }
        })
        print("Delete Acknowledged : ",result.acknowledged)
        self.__ef_db.ef_update_flat_rate(flat_number=flat, rate=0.0)
        self.__flats_db.change_occupied_status(flat=flat,status=False)
    
    def get_all_members(self):
        data=[]
        for member in self.__members_collection.find({}):
            data.append({
                "name":member["OWNER_NAME"],
                "emails":member["EMAILS"],
                "flat":member["FLT_NUMS"],
                "is_admin":member['ADMIN_ACCESS']})
        return data
