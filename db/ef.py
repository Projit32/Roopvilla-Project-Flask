from db.client import MongoDBClient
import math

class EmergencyFundFunctions:
    __flats_collections=MongoDBClient.flats
    __ef_collection=MongoDBClient.emergency_funds
    __alternate_round = lambda amount: (math.floor(amount) if(((amount*10.0)%10)<5) else math.ceil(amount))

    def ef_initialization(self, superbuild_factor=25):
        EmergencyFundFunctions.__ef_collection.drop()
        data_list=list()
        flats = self.__flats_collections.find({})
        for flat in flats:
            flat_data={
                "FLT_NUM":flat['FLT_NUM'],
                "FLT_TLT_AREA":flat['FLT_TLT_AREA'],
                "SPR_BLD_FACTOR":superbuild_factor,
                "CRPT_AREA":flat['CRPT_AREA'],
                "RATE": 0.000,
                "TLT_AMNT": 0.000000,
                "RND_OFF_AMNT":0
            }
            data_list.append(flat_data)
            
        # Insertion
        result=EmergencyFundFunctions.__ef_collection.insert_many(data_list)
        return result

    def ef_update_flat_rate(self, flat_number, rate=0.0):
        for data in EmergencyFundFunctions.__ef_collection.find({"FLT_NUM":flat_number}):
            amount = data['CRPT_AREA']*rate
            result=EmergencyFundFunctions.__ef_collection.update_one({"FLT_NUM":flat_number},{
                    "$set": {
                        "RATE": rate,
                        "TLT_AMNT": amount,
                        "RND_OFF_AMNT": EmergencyFundFunctions.__alternate_round(amount)
                    }
                })
            print("EF UPDATE- Matched :",result.matched_count)
            print("EF UPDATE- Modified :",result.modified_count)
    
    def get_ef_details(self):
        response=[]
        for data in EmergencyFundFunctions.__ef_collection.find({}):
            item={
                "flat":data['FLT_NUM'],
                "rate":data['RATE']
            }
            response.append(item)
        return response