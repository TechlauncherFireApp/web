import json

from flask import Blueprint
from flask_restful import reqparse, Resource, fields, marshal_with, Api

from domain import session_scope
from repository.question_repository import *


parser = reqparse.RequestParser()
parser.add_argument('id', action='store', type=str)

question_fields = {
    "id": fields.Integer,
    "description": fields.String
}


class QuestionRequest(Resource):
    @marshal_with(question_fields)
    def get(self):
        args = parser.parse_args()
        if args["id"] is None:
            return
        with session_scope() as session:
            question = get_question_by_id(session, args["id"])
            print(json.loads(question.choice))
            return question


question_bp = Blueprint('getQuestionByI', __name__)
api = Api(question_bp)
api.add_resource(QuestionRequest, "/quiz/getQuestionById")
