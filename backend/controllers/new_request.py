from flask import Blueprint
from flask_restful import reqparse, Resource, fields, marshal_with, Api

from domain import session_scope
from repository.request_repository import *

'''
Define Data Input

{
    "title": String
}
'''

parser = reqparse.RequestParser()
parser.add_argument('title', action='store', type=str)

'''
Define Data Output

{
    "id": String
}
'''

resource_fields = {
    "id": fields.String
}


# Make a New Request inside the DataBase
class NewRequest(Resource):
    @marshal_with(resource_fields)
    def post(self):
        args = parser.parse_args()
        if args["title"] is None:
            return
        with session_scope() as session:
            new_id = new_request(session, args["title"])
            return {"id": new_id}


new_request_bp = Blueprint('new_requests', __name__)
api = Api(new_request_bp)
api.add_resource(NewRequest, "/new_request")
