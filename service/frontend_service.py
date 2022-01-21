from flask import request, Blueprint, render_template, session
from util.jwt_functions import authenticate
import traceback 
 
frontend_pages = Blueprint('frontend_pages', __name__ , template_folder='templates', static_folder='static')

@frontend_pages.route('/', methods=['GET'])
def login_page():
    return render_template('login.html')

@frontend_pages.route('/home', methods=['GET'])
def test():
    return {"KEY": session['token']}
