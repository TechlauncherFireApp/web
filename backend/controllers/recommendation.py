from flask import Blueprint
from flask_restful import reqparse, Resource, fields, marshal_with, Api

from repository.asset_request_vehicle_repository import get_vehicles
from repository.asset_request_volunteer_repository import add_shift
from .utility import *
from services.optimiser import schedule
from repository.volunteer_repository import *
from domain import session_scope

parser = reqparse.RequestParser()
parser.add_argument('requestId', action='append', type=int)

'''
Define data output

{
    "results" : [{
        "shiftID": String
        "assetClass": String [lightUnit | mediumTanker | heavyTanker]
        "startTime": DateTimeString iso8601,
        "endTime": DateTimeString iso8601,
        "volunteers": {
            "ID": String,
            "positionID": Integer,
            "role": [String]
        }
    }]
}
'''

volunteer_field = {
    'ID': fields.String,
    'positionID': fields.Integer,
    'role': fields.List(fields.String)
}

recommendation_list_field = {
    'shiftID': fields.String,
    'assetClass': fields.String,
    'startTime': fields.DateTime(dt_format='iso8601', attribute=lambda x: x['timeframe'][0]),
    'endTime': fields.DateTime(dt_format='iso8601', attribute=lambda x: x['timeframe'][1]),
    'volunteers': fields.List(fields.Nested(volunteer_field))
}

resource_fields = {
    'results': fields.List(fields.Nested(recommendation_list_field))
}


# Handle the Recommendation endpoint
class Recommendation(Resource):

    @marshal_with(resource_fields)
    def get(self):
        args = parser.parse_args()
        if args["requestId"] is None:
            return

        with session_scope() as session:
            asset_requests = []
            vehicles = get_vehicles(session, args['requestId'])
            for vehicle in vehicles:
                vehicle_id, asset_class, start_date, end_date = vehicle
                asset_requests.append({
                    "shiftID": vehicle_id,
                    "assetClass": asset_class,
                    "timeframe": (start_date, end_date)
                })
            volunteers = list_volunteers(session)

            # Get the generated recommendation
            output = schedule(volunteers, asset_requests)

            if not output == []:
                print("Optimisation Succeeded")

            # Persist the optimisation! we don't ask the fkn front end to manage the backends data! This is completely
            # insane and the reason the front end is a cluster fk!
            for vehicle in output:
                vehicle_id = vehicle['shiftID']
                for volunteer in vehicle['volunteers']:
                    volunteer_id = volunteer['ID']
                    if volunteer_id == -1:
                        volunteer_id = None
                    position = volunteer['positionID']
                    role = volunteer['role']
                    add_shift(session, volunteer_id, vehicle_id,position, role)
            return {"results": output}


recommendation_bp = Blueprint('recommendation', __name__)
api = Api(recommendation_bp)
api.add_resource(Recommendation, '/recommendation')
