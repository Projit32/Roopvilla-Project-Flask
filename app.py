from flask import Flask, session
from datetime import timedelta
from flask_session import Session
from pymongo import MongoClient
from service import user_service, ef_service, member_service, monthly_service, frontend_service, moms_service, features_service, sessions_service, flats_service, estimate_services, expense_services
import os


flask_app = Flask(__name__)
flask_app.config["SECRET_KEY"] = os.getenv('SESSION_SECRET')
flask_app.config["SESSION_USE_SIGNER"] = True
flask_app.config["SESSION_PERMANENT"] = True
flask_app.config["PERMANENT_SESSION_LIFETIME"] = timedelta(hours=1)
flask_app.config["SESSION_TYPE"] = "mongodb"
flask_app.config["SESSION_MONGODB"] = MongoClient(os.getenv('MONGO_DB'),connect=False)
flask_app.config["SESSION_MONGODB_DB"] = "roopvilla_maintenance"
flask_app.config["SESSION_MONGODB_COLLECT"] ="psessions"
Session(flask_app)

flask_app.register_blueprint(expense_services.expenses_apis)
flask_app.register_blueprint(estimate_services.estimates_apis)
flask_app.register_blueprint(flats_service.flats_apis)
flask_app.register_blueprint(sessions_service.sessions_apis)
flask_app.register_blueprint(moms_service.moms_apis)
flask_app.register_blueprint(features_service.features_apis)
flask_app.register_blueprint(ef_service.ef_apis)
flask_app.register_blueprint(user_service.user_apis)
flask_app.register_blueprint(member_service.member_apis)
flask_app.register_blueprint(monthly_service.monthly_apis)
flask_app.register_blueprint(frontend_service.frontend_pages)


if __name__ == '__main__':
    flask_app.run(port=int(os.getenv('PORT')), debug=False)