from flask import Blueprint
from flask_restful import reqparse, Resource, fields, marshal_with, Api

from services.optimiser import Optimiser
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
            o = Optimiser(session, args['requestId'], False)
            result = o.solve()
            print(result)
            o.save_result(session, result)
            return {"results": result is not None}


recommendation_bp = Blueprint('recommendation', __name__)
api = Api(recommendation_bp)
api.add_resource(Recommendation, '/recommendation')
