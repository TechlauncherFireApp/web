from flask import Blueprint
from flask_restful import Resource, fields, marshal_with, Api

from ..domain import session_scope
from ..repository import get_existing_requests

'''
Define Data Output

GET
{
    "id": String,
    "title": String
}

'''

get_resource_obj = {
    "id": fields.String,
    "title": fields.String
}

get_resource_list = {
    "success": fields.Boolean,
    "results": fields.List(fields.Nested(get_resource_obj))
}


# Handle the Recommendation endpoint
class ExistingRequests(Resource):
    @marshal_with(get_resource_list)
    def get(self):
        with session_scope() as session:
            res = get_existing_requests(session)
            return {"success": True, "results": res}


existing_requests_bp = Blueprint('existing_requests', __name__)
api = Api(existing_requests_bp)
api.add_resource(ExistingRequests, '/existing_requests')
