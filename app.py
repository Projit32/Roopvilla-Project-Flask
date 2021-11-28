from flask import Flask, jsonify
from flask_restful import Api
from resources import ef, memebers, monthly, user
import os


app = Flask(__name__)
api = Api(app)

api.add_resource(ef.EmergencyFunds, '/emergencyFunds')
api.add_resource(memebers.Members, '/members')
api.add_resource(monthly.Months, '/months')
api.add_resource(user.Users, '/users')


if __name__ == '__main__':
    app.run(port=int(os.getenv('PORT')), debug=False)