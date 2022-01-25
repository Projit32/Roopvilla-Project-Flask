from flask import request, Blueprint, render_template, session
from util.jwt_functions import authenticate
import traceback 
 
frontend_pages = Blueprint('frontend_pages', __name__ , static_folder='static',static_url_path='/../static')

@frontend_pages.route('/', methods=['GET'])
def login_page():
    return render_template('login.html',)

@frontend_pages.route('/home', methods=['GET'])
@authenticate
def home_page():
    return render_template('home.html',path="home",name=request.args.get("ADM_NAME"))

@frontend_pages.route('/monthlyActions', methods=['GET'])
#@authenticate
def home_page():
    return render_template('monthly.html',path="monthlyActions",name=request.args.get("ADM_NAME"))


@frontend_pages.route('/emergencyFunds', methods=['GET'])
@authenticate
def ef_page():
    return render_template('ef.html',path="emergencyFunds",name=request.args.get("ADM_NAME"))

@frontend_pages.route('/memberDetails', methods=['GET'])
@authenticate
def members_page():
    return render_template('members.html',path="memberDetails",name=request.args.get("ADM_NAME"))
