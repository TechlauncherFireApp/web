from flask import Blueprint
from flask_restful import reqparse, Resource, fields, marshal_with, Api

from repository.asset_request_vehicle_repository import get_vehicles
from repository.asset_request_volunteer_repository import add_shift
from services.optimiser2.optimiser import Optimiser
from .utility import *
from services.optimiser import schedule
from repository.volunteer_repository import *
from domain import session_scope

parser = reqparse.RequestParser()
parser.add_argument('requestId', action='append', type=int)

resource_fields = {
    'results': fields.Boolean
}


# Handle the Recommendation endpoint
class Recommendation(Resource):

    @marshal_with(resource_fields)
    def get(self):
        args = parser.parse_args()
        if args["requestId"] is None:
            return

        with session_scope() as session:
            optimiser = Optimiser(session, args['requestId'], True)
            # Attempt a full model
            model = optimiser.generate_model_string(True)
            result = optimiser.solve(model)
            print(result, result is None)
            if result.solution:
                optimiser.save_result(session, result)
            else:
                # Attempt a partial model
                model = optimiser.generate_model_string(False)
                result = optimiser.solve(model)
                if result.solution:
                    optimiser.save_result(session, result)
                else:
                    optimiser.save_empty_result(session)

            return {"results": result is not None}


recommendation_bp = Blueprint('recommendation', __name__)
api = Api(recommendation_bp)
api.add_resource(Recommendation, '/recommendation')
