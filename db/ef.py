from db.client import MongoDBClient
import math

class EmergencyFundFunctions:
    _flats =['Ground','1A','1B','2A','2B','3A','3B','4A','4B','5A','5B','6']
    _total_area=[440,1460,940,1460,940,1628,772,1460,940,1460,940,475]
    _ef_collection=MongoDBClient.emergency_funds
    _alternate_round = lambda amount: (math.floor(amount) if(((amount*10.0)%10)<5) else math.ceil(amount))

    def ef_initialization(self, superbuild_factor=25):
        EmergencyFundFunctions._ef_collection.drop()
        data_list=list()
        for i in range(len(EmergencyFundFunctions._flats)):
            flat_data={
                "FLT_NUM":EmergencyFundFunctions._flats[i],
                "FLT_TLT_AREA":EmergencyFundFunctions._total_area[i],
                "SPR_BLD_FACTOR":superbuild_factor,
                "CRPT_AREA":(EmergencyFundFunctions._total_area[i]-((EmergencyFundFunctions._total_area[i])*(superbuild_factor/100))),
                "RATE": 0.000,
                "TLT_AMNT": 0.000000,
                "RND_OFF_AMNT":0
            }
            data_list.append(flat_data)
            
        # Insertion
        result=EmergencyFundFunctions._ef_collection.insert_many(data_list)
        return result

    def ef_update_flat_rate(self, flat_number, rate=0.0):
        for data in EmergencyFundFunctions._ef_collection.find({"FLT_NUM":flat_number}):
            amount = data['CRPT_AREA']*rate
            result=EmergencyFundFunctions._ef_collection.update_one({"FLT_NUM":flat_number},{
                    "$set": {
                        "RATE": rate,
                        "TLT_AMNT": amount,
                        "RND_OFF_AMNT": EmergencyFundFunctions._alternate_round(amount)
                    }
                })
            print("EF UPDATE- Matched :",result.matched_count)
            print("EF UPDATE- Modified :",result.modified_count)
    
    def get_ef_details(self):
        response=[]
        for data in EmergencyFundFunctions._ef_collection.find({}):
            item={
                "flat":data['FLT_NUM'],
                "rate":data['RATE']
            }
            response.append(item)
        return response