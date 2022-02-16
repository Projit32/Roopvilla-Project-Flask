from db.client import MongoDBClient
from util.api_exceptions import RequestException

class FlatsFunctions:
    __flats_db=MongoDBClient.flats

    def change_occupied_status(self, flat, status=False):
        result = self.__flats_db.update_one({'FLT_NUM':flat},{
            '$set':{
                "OCCUPIED":status
            }
        },upsert=False)
        print("Change Flat Occupied status ", result.modified_count)
    
    def get_occupied_status(self, flat):
        result = self.__flats_db.find_one({'FLT_NUM':flat})
        if result is not None:
            return result['OCCUPIED']
        else:
            raise RequestException('No Such Flat Exists!')
    
    def get_unoccupied_flats(self):
        result = self.__flats_db.find({"OCCUPIED":False})
        flats=list()
        for item in result:
            flats.append(item['FLT_NUM'])
        return flats
