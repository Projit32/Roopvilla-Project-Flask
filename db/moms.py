from db.client import MongoDBClient


from util.api_exceptions import RequestException

class MinutesOfMeetingFunctions:

    __moms_collection=MongoDBClient.moms

    def insert_mom(self, date, moms=[]):
        if MinutesOfMeetingFunctions.__moms_collection.find_one({"Date":date}) is not None:
            raise RequestException("MOM record exisits for this Date!")
        data={
            "DATE": date,
            "MOMS":moms
        }
        result=MinutesOfMeetingFunctions.__moms_collection.insert_one(data)
        print("New MOM Acknowledged : ",result.acknowledged, result.inserted_id)

    def delete_mom(self, date):
        result=MinutesOfMeetingFunctions.__moms_collection.delete_one({"DATE": date})
        print("MOM Deleted:",result.acknowledged, result.deleted_count)
    
    def get_mom(self, start, end):
        result = MinutesOfMeetingFunctions.__moms_collection.find({
            "DATE":{
                "$gte":start,
                "$lte":end
            }
        }).sort("DATE")
        data =[]
        for item in result:
            mom_list=[]
            for top_dis in item['MOMS']:
                mom_list.append({
                    "topic":top_dis["TOPIC"],
                    "decision":top_dis["DECISION"]
                })
            data.append({
                "date":item['DATE'],
                "mom":mom_list
            })

        return data
