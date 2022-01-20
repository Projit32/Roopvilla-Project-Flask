from flask import request, Blueprint
from db.monthly import MonthlyFunctions
from util.jwt_functions import authenticate
import traceback

_monthly_db=MonthlyFunctions()
_months=["JAN","FEB","MAR","APR","MAY","JUN","JUL","AUG","SEP","OCT","NOV","DEC"]
monthly_apis = Blueprint('monthly_apis', __name__)

@monthly_apis.route('/months', methods=['POST'])
@authenticate
def create_monthly_dist():
    requestData=request.get_json()
    queryParams=request.args
    try:
        month=_months[int(queryParams.get('month'))-1]
        year=int(queryParams.get('year'))
        print(month,year)
        _monthly_db.create_monthly_dist(month=month,year=year,est=requestData['estimates'],flats=requestData['payingFlats'])
        _monthly_db.populate_unsold(month=month,year=year,flats=requestData['unsoldFlats'])
        _monthly_db.idiot_box(month=month,year=year, flats=requestData['notPayingFlats'])
    except Exception as err:
        traceback.print_exc()
        print(err, type(err))
        return {"message": "An error occurred Creating Monthly Distribution"}, 500
    return "",201

@monthly_apis.route('/months/paymentStatus', methods=['PATCH'])
@authenticate
def update_payments():
    requestData=request.get_json()
    queryParams=request.args
    try:
        month=_months[int(queryParams.get('month'))-1]
        year=int(queryParams.get('year'))
        _monthly_db.update_payment_status(month=month,year=year,flats=requestData['flats'],status=requestData['status'])
    except Exception as err:
        traceback.print_exc()
        print(err, type(err))
        return {"message": "An error occurred updating payments"}, 500
    return "",204

@monthly_apis.route('/months/expenses', methods=['PUT'])
@authenticate
def update_expenses():
    requestData=request.get_json()
    queryParams=request.args
    try:
        monthNumber=int(queryParams.get('month'))
        month=_months[monthNumber-1]
        prev=_months[monthNumber-2]
        curr_year=int(queryParams.get('year'))
        prev_year = curr_year-1 if monthNumber == 1 else curr_year
        el_meter=requestData['electricity']
        _monthly_db.update_expenses(month=month,prev_month=prev,year=curr_year,prev_year=prev_year,el_month=_months[int(el_meter['month'])-1],el_year=int(el_meter['year']),el_amount=int(el_meter['amount']),el_unit=int(el_meter['units']),exp=requestData['expenditures'])
    except Exception as err:
        traceback.print_exc()
        print(err, type(err))
        return {"message": "An error occurred updating expenses"}, 500
    return "",204

@monthly_apis.route('/months/defaulters', methods=['OPTIONS'])
@authenticate
def populate_defaulter():
    requestData=request.get_json()
    queryParams=request.args
    try:
        monthNumber=int(queryParams.get('month'))
        month=_months[monthNumber-1]
        year=int(queryParams.get('year'))
        _monthly_db.populate_defaulter(month=month,year=year,flats=requestData['flats'])
    except Exception as err:
        traceback.print_exc()
        print(err, type(err))
        return {"message": "An error occurred populating defaulters"}, 500
    return "",204

@monthly_apis.route('/months', methods=['DELETE'])
@authenticate
def delete_monthly_data():
    queryParams=request.args
    try:
        monthNumber=int(queryParams.get('month'))
        month=_months[monthNumber-1]
        year=int(queryParams.get('year'))
        _monthly_db.delete_monthly_data(month=month,year=year)
    except Exception as err:
        traceback.print_exc()
        print(err, type(err))
        return {"message": "An error occurred Deleting Monthly Distribution"}, 500
    return "",204