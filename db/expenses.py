from tkinter import N
from db.client import MongoDBClient
from bson import ObjectId

'''
Need to complete it.
'''
class ExpensesFunctions:
    __expenses_db=MongoDBClient.expenses

    def add_expenses(self, name, amount, type, month, year):
        estimate ={
            "NAME": name,
            "TYPE": type,
            "AMOUNT": amount,
            "MONTH": month,
            "YEAR": year,
        }
        results=self.__expenses_db.insert_one(estimate)
        print("Fixed expenses Insert Acknowledged: ",results.acknowledged)
        print("Fixed expenses Insert ID: ",results.inserted_id)

    def delete_expenses(self, month, year):
        result=self.__expenses_db.delete_one({"MONTH": month, "YEAR":year})
        print("Fixed expenses Deleted: ",result.acknowledged)
        print("Fixed expenses delete count: ",result.deleted_count)

    def get_expenses(self, month=None, year=None) -> list:
        search_filters={}
        if month is not None:
            search_filters['MONTH']=month
        if year is not None:
            search_filters['YEAR']=year
        result = self.__expenses_db.find(search_filters)
        expenses=[]
        for item in result:
            expense={
                "name": item["NAME"],
                "type": item["TYPE"],
                "amount": item["AMOUNT"],
                "month": item['MONTH'],
                "year": item["YEAR"],
                "id": str(item["_id"])
            }
            expenses.append(expense)
        return expenses