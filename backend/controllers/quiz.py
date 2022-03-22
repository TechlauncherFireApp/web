from flask import Blueprint
from flask_restful import reqparse, Resource, fields, marshal_with, Api

from domain import session_scope
from repository.question_repository import *
from domain.type.question_type import QuestionType


question_fields = {
    "id": fields.Integer,
    "description": fields.String,
    "choice": fields.List(fields.Raw)
}


class GetQuestionRequest(Resource):
    @marshal_with(question_fields)
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('id', type=int, required=True)
        args = parser.parse_args()
        with session_scope() as session:
            return get_question_by_id(session, args["id"])


class GetQuestionListRequest(Resource):
    @marshal_with(question_fields)
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('num', type=int)
        num = parser.parse_args()["num"]
        if num is None:
            num = 10
        with session_scope() as session:
            return get_question_list(session, num)


question_bp = Blueprint('QuizRequest', __name__)
api = Api(question_bp, "/quiz")
api.add_resource(GetQuestionRequest, "/getQuestionById")
api.add_resource(GetQuestionListRequest, "/getQuestionList")
