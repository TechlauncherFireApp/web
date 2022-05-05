from flask import Blueprint, request, jsonify
from flask_restful import reqparse, Resource, fields, marshal_with, Api, inputs
from domain import session_scope
from repository.unavailability_repository import *

select_parser = reqparse.RequestParser()
select_parser.add_argument('userId', type=int, required=True)

# change variable names
create_parser = reqparse.RequestParser()
create_parser.add_argument('userId', type=int, required=True)
create_parser.add_argument('title', type=str, required=True)
create_parser.add_argument('periodicity', type=int, required=True)
create_parser.add_argument('start',type=inputs.datetime_from_iso8601, required=True)
create_parser.add_argument('end',type=inputs.datetime_from_iso8601, required=True)

remove_parser = reqparse.RequestParser()
remove_parser.add_argument('userId', type=int, required=True)
remove_parser.add_argument('eventId', type=int, required=True)

userEvent_fields = {
    "userId": fields.Integer,
    "title": fields.String,
    "start": fields.DateTime(dt_format='iso8601'),
    "end": fields.DateTime(dt_format='iso8601'),
    "periodicity": fields.Integer
}

class ShowUnavailabilityEvent(Resource):
    @marshal_with(userEvent_fields)
    def get(self):
        args = select_parser.parse_args()
        with session_scope() as session:
            user_events = fetch_event(session, args['userId'])
            if user_events is None:
                return jsonify({"userId": args['userId'], "success": False})
            return user_events

class CreateNewUnavailabilityEvent(Resource):
    def post(self):
        request.get_json(force=True)
        args = create_parser.parse_args()
        with session_scope() as session:
            eventId = create_event(session, args['userId'], args['title'],
                                args['start'], args['end'], args['periodicity'])
            if eventId is None:
                return jsonify({"eventId": -1,
                        "success": False})
            return jsonify({"eventId": eventId,
                            "success": True})

class RemoveUnavailabilityEvent(Resource):
    def get(self):
        args = remove_parser.parse_args()
        with session_scope() as session:
            return {"success": remove_event(session, args['userId'], args['eventId'])}

volunteer_unavailability_bp = Blueprint('volunteer_unavailability', __name__)
api = Api(volunteer_unavailability_bp, '/unavailability')
api.add_resource(ShowUnavailabilityEvent, '/showUnavailableEvent')
api.add_resource(CreateNewUnavailabilityEvent, '/createUnavailableEvent')
api.add_resource(RemoveUnavailabilityEvent, '/removeUnavailableEvent')
