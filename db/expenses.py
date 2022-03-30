from db.client import MongoDBClient
from bson import ObjectId

'''
Need to complete it.
'''
class ExpensesFunctions:
    __expenses_db=MongoDBClient.expenses

    def add_expenses(self, name, amount, type):
        estimate ={
            "NAME": name,
            "TYPE": "FXD",
        }
        results=self.__expenses_db.insert_one(estimate)
        print("Fixed expenses Insert Acknowledged: ",results.acknowledged)
        print("Fixed expenses Insert ID: ",results.inserted_id)

    def edit_expenses(self, id, name, amount, type):
        estimate ={
            "NAME": name,
            "TYPE": "FXD",
        }
        results=self.__expenses_db.replace_one({"_id":ObjectId(id)},estimate)
        print("Fixed expenses Update Acknowledged: ",results.acknowledged)
        print("Fixed expenses Update Matched", results.matched_count)
        print("Fixed expenses Update Modified", results.modified_count)

    def delete_expenses(self, month, year):
        result=self.__expenses_db.delete_one({"MONTH": month, "YEAR":year})
        print("Fixed expenses Deleted: ",result.acknowledged)
        print("Fixed expenses delete count: ",result.deleted_count)

    def get_expenses(self):
        pass