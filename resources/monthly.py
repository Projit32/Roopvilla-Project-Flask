from flask_restful import Resource
from flask import request
from db.monthly import MonthlyFunctions

class Months(Resource):
    _monthly_db=MonthlyFunctions()
    _months=["JAN","FEB","MAR","APR","MAY","JUN","JUL","AUG","SEP","OCT","NOV","DEC"]
    def post(self):
        requestData=request.get_json()
        queryParams=request.args
        try:
            month=Months._months[int(queryParams.get('month'))-1]
            year=queryParams.get('year')
            print(month,year)
            Months._monthly_db.create_monthly_dist(month=month,year=year,est=requestData['estimates'],flats=requestData['payingFlats'])
            Months._monthly_db.populate_unsold(month=month,year=year,flats=requestData['unsoldFlats'])
            Months._monthly_db.idiot_box(month=month,year=year, flats=requestData['notPayingFlats'])
        except Exception as err:
            print(err, type(err))
            return {"message": "An error occurred Creating Monthly Distribution"}, 500
        return {},201
    
    def put(self):
        requestData=request.get_json()
        queryParams=request.args
        try:
            month=Months._months[int(queryParams.get('month'))-1]
            year=queryParams.get('year')
            Months._monthly_db.update_payment_status(month=month,year=year,flats=requestData['flats'])
        except Exception as err:
            print(err, type(err))
            return {"message": "An error occurred Creating Monthly Distribution"}, 500
        return {},200
    
    def patch(self):
        requestData=request.get_json()
        queryParams=request.args
        try:
            monthNumber=int(queryParams.get('month'))
            month=Months._months[monthNumber-1]
            prev=Months._months[monthNumber-2]
            curr_year=queryParams.get('year')
            prev_year = curr_year-1 if monthNumber == 1 else curr_year
            Months._monthly_db.update_expenses(month=month,prev_month=prev,year=curr_year,prev_year=prev_year,exp=requestData['expenditures'])
        except Exception as err:
            print(err, type(err))
            return {"message": "An error occurred Creating Monthly Distribution"}, 500
        return {},200
    
    def options(self):
        requestData=request.get_json()
        queryParams=request.args
        try:
            monthNumber=int(queryParams.get('month'))
            month=Months._months[monthNumber-1]
            year=queryParams.get('year')
            Months._monthly_db.populate_defaulter(month=month,year=year,flats=requestData['flats'])
        except Exception as err:
            print(err, type(err))
            return {"message": "An error occurred Creating Monthly Distribution"}, 500
        return {},200
    
    def delete(self):
        queryParams=request.args
        try:
            monthNumber=int(queryParams.get('month'))
            month=Months._months[monthNumber-1]
            year=queryParams.get('year')
            Months._monthly_db.delete_monthly_data(month=month,year=year)
        except Exception as err:
            print(err, type(err))
            return {"message": "An error occurred Creating Monthly Distribution"}, 500
        return {},200