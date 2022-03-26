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

result_fields = {
    "result": fields.Boolean
}

create_question_fields = {
    "question_id": fields.Integer
}


class GetQuestionRequest(Resource):
    @marshal_with(question_fields)
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('id', type=int, required=True)
        args = parser.parse_args()
        with session_scope() as session:
            return get_question_by_id(session, args["id"])


class GetRandomQuestionRequest(Resource):
    @marshal_with(question_fields)
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('num', type=int)
        parser.add_argument('role', type=str, default='volunteer')
        parser.add_argument('difficulty', type=int, default=1)
        args = parser.parse_args()
        num = args['num']
        if num is None:
            num = 10
        with session_scope() as session:
            return get_random_question(session, num, args['role'], args['difficulty'])


class DeleteQuestion(Resource):
    @marshal_with(result_fields)
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('id', type=int, required=True)
        question_id = parser.parse_args()["id"]
        with session_scope() as session:
            return {'result': delete_question(session, question_id)}


class CreateQuestion(Resource):
    @marshal_with(create_question_fields)
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('question_type', type=int, required=True)
        parser.add_argument('role', type=str)
        parser.add_argument('description', type=str, required=True)
        parser.add_argument('choice', type=str, required=True)
        parser.add_argument('difficulty', type=int, required=True)
        parser.add_argument('answer', type=str, required=True)
        question_type = QuestionType(parser.parse_args()["question_type"])
        role = parser.parse_args()["role"]
        description = parser.parse_args()["description"]
        choice = parser.parse_args()["choice"]
        difficulty = parser.parse_args()["difficulty"]
        answer = parser.parse_args()["answer"]
        with session_scope() as session:
            return {'question_id': create_question(session, question_type, role, description,
                                                   choice, difficulty, answer)}


class UpdateQuestion(Resource):
    @marshal_with(result_fields)
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('id', type=int, required=True)
        parser.add_argument('role', type=str)
        parser.add_argument('description', type=str)
        parser.add_argument('choice', type=str)
        parser.add_argument('difficulty', type=int)
        parser.add_argument('answer', type=str)
        question_id = parser.parse_args()["id"]
        role = parser.parse_args()["role"]
        description = parser.parse_args()["description"]
        choice = parser.parse_args()["choice"]
        difficulty = parser.parse_args()["difficulty"]
        answer = parser.parse_args()["answer"]
        with session_scope() as session:
            return {'result': update_question(session, question_id, role, description,
                                              choice, difficulty, answer)}


class CheckAnswer(Resource):
    @marshal_with(result_fields)
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('id', type=int, required=True)
        parser.add_argument('answer', type=str)
        question_id = parser.parse_args()["id"]
        answer = parser.parse_args()["answer"]
        with session_scope() as session:
            return {"result": check_answer(session, question_id, answer)}


tutorial_quiz_bp = Blueprint('tutorial_quiz', __name__)
api = Api(tutorial_quiz_bp, "/quiz")
api.add_resource(GetQuestionRequest, "/getQuestionById")
api.add_resource(GetRandomQuestionRequest, "/getRandomQuestion")
api.add_resource(DeleteQuestion, "/deleteQuestion")
api.add_resource(CreateQuestion, "/createQuestion")
api.add_resource(UpdateQuestion, "/updateQuestion")
api.add_resource(CheckAnswer, "/checkAnswer")
