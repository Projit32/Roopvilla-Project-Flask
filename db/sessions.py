from db.client import MongoDBClient
from datetime import datetime, timezone

class SessionFunctions:
    __node_session_db=MongoDBClient.nsessions
    __flask_session_db=MongoDBClient.psessions

    def get_expired_sessions(self):
        expired_sessions=0
        expired_sessions+= len(list(self.__node_session_db.find({"expires":{
            "$lt": datetime.now(timezone.utc)
        }})))
        expired_sessions+= len(list(self.__flask_session_db.find({"expiration":{
            "$lt": datetime.now(timezone.utc)
        }})))

        return expired_sessions
    
    def delete_expired_sessions(self):
        result=self.__node_session_db.delete_many({"expires":{
            "$lt": datetime.now(timezone.utc)
        }})
        print("Node session Deleted: ",result.deleted_count)

        result=self.__flask_session_db.delete_many({"expiration":{
            "$lt": datetime.now(timezone.utc)
        }})
        print("Flask session Deleted: ",result.deleted_count)