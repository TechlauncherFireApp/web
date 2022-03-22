from flask import Blueprint
from flask_restful import reqparse, Resource, fields, marshal_with, Api

from domain import session_scope
from repository.question_repository import *

parser = reqparse.RequestParser()
parser.add_argument('id', action='store', type=str)
parser.add_argument('num', action='store', type=str)

question_fields = {
    "id": fields.Integer,
    "description": fields.String,
    "choice": fields.List(fields.Raw)
}


class GetQuestionRequest(Resource):
    @marshal_with(question_fields)
    def get(self):
        args = parser.parse_args()
        if args["id"] is None:
            return
        with session_scope() as session:
            question = get_question_by_id(session, args["id"])
            return question


class GetQuestionListRequest(Resource):
    @marshal_with(question_fields)
    def get(self):
        num = parser.parse_args()["num"]
        if num is None:
            num = 10
        with session_scope() as session:
            questions = get_question_list(session, num)
            return questions


question_bp = Blueprint('QuizRequest', __name__)
api = Api(question_bp, "/quiz")
api.add_resource(GetQuestionRequest, "/getQuestionById")
api.add_resource(GetQuestionListRequest, "/getQuestionList")
