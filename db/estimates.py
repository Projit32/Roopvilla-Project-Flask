from unittest import result
from db.client import MongoDBClient
from bson import ObjectId

class EstimatesFunctions:
    __fixed_estimates_db=MongoDBClient.fixed_estimates

    def add_estimates(self, name, monthly, annually):
        estimate ={
            "NAME": name,
            "TYPE": "FXD",
            "MOTHLY": float(monthly),
            "ANNUALLY": float(annually)
        }
        results=self.__fixed_estimates_db.insert_one(estimate)
        print("Fixed Estimates Insert Acknowledged: ",results.acknowledged)
        print("Fixed Estimates Insert ID: ",results.inserted_id)

    def edit_estimates(self, id, name, monthly, annually):
        estimate ={
            "NAME": name,
            "TYPE": "FXD",
            "MOTHLY": float(monthly),
            "ANNUALLY": float(annually)
        }
        results=self.__fixed_estimates_db.replace_one({"_id":ObjectId(id)},estimate)
        print("Fixed Estimates Update Acknowledged: ",results.acknowledged)
        print("Fixed Estimates Update Matched", results.matched_count)
        print("Fixed Estimates Update Modified", results.modified_count)

    def delete_estimates(self, id):
        result=self.__fixed_estimates_db.delete_one({"_id":ObjectId(id)})
        print("Fixed Estimates Deleted: ",result.acknowledged)
        print("Fixed Estimates delete count: ",result.deleted_count)

    def get_estimates(self):
        result = self.__fixed_estimates_db.find({})
        estimates=[]
        for item in result:
            estimate={
                "name": item["NAME"],
                "monthly": item["MOTHLY"],
                "annually": item["ANNUALLY"],
                "id": str(item["_id"])
            }
            estimates.append(estimate)
        return estimates
