from flask_restful import Resource, reqparse
from db.ef import EmergencyFundFunctions


class EmergencyFunds(Resource):
    _ef_db= EmergencyFundFunctions()
    _ef_Parser  = reqparse.RequestParser()
    _ef_Parser.add_argument('flat_number',
                            type=str,
                            required=True,
                            help="Need a Flat Number to update the rate"
                            )
    _ef_Parser.add_argument('rate',
                            type=float,
                            required=True,
                            help="Rate x 0.XX times"
                            )
    def post(self):
        try:
            result = EmergencyFunds._ef_db.ef_initialization()
            return {"Created":"YES"}, 201
        except Exception as err:
            print(err, type(err))
            return {"message": "An error occurred creating EF."}, 500

    
    def put(self):
        data= EmergencyFunds._ef_Parser.parse_args()
        EmergencyFunds._ef_db.ef_update_flat_rate(**data)
        return {"Updated": "YES"}, 200

