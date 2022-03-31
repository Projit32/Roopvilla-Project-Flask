from flask import request, Blueprint
from db.expenses import ExpensesFunctions
from datetime import datetime
from util.jwt_functions import authenticate
import traceback 
 
__expenses_db= ExpensesFunctions()
expenses_apis = Blueprint('expenses_apis', __name__)

@expenses_apis.route('/expenses', methods=['POST'])
@authenticate
def create_expenses():
    try:
        data=request.get_json()
        __expenses_db.add_expenses(name=data['name'], amount=float(data['amount']), type=data['type'], month=data['month'], year=int(data['year']))
        return {}, 201
    except Exception as err:
        traceback.print_exc()
        print(err, type(err))
        return {"error": "An error occurred creating Expenses."}, 500


@expenses_apis.route('/expenses', methods=['DELETE'])
@authenticate
def delete_expenses():
    try:
        queryParams=request.args
        month= queryParams.get('month')
        year=int(queryParams.get('year')) if queryParams.get('year') is not None else None
        __expenses_db.delete_expenses(month=month, year=year)
        return "", 204
    except Exception as err:
        traceback.print_exc()
        print(err, type(err))
        return {"error": "An error occurred Deleting Expenses."}, 500

@expenses_apis.route('/expenses', methods=['GET'])
@authenticate
def get_expenses():
    try:
        queryParams=request.args
        month= queryParams.get('month')
        year=int(queryParams.get('year')) if queryParams.get('year') is not None else None
        value =__expenses_db.get_expenses(month=month, year=year)
        return {"data":value}, 200
    except Exception as err:
        traceback.print_exc()
        print(err, type(err))
        return {"error": "An error occurred Fetching Expenses."}, 500