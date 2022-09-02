from flask import Blueprint, request, jsonify
from flask_restful import fields, Resource, marshal_with, Api, reqparse

from domain import session_scope
import repository.chatbot_input_repository as chatbot_input_repository


class GetChatInputRequest(Resource):
    chatbot_input_fields = {
        'created_time': fields.String,
        'content': fields.String
    }

    @marshal_with(chatbot_input_fields)
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('email', type=str)
        args = parser.parse_args()
        with session_scope() as session:
            return chatbot_input_repository.get_input_by_user_email(session, args['email'])


class AddChatInputRequest(Resource):
    add_input_result = {
        'result': fields.Boolean,
        'reason': fields.String
    }

    @marshal_with(add_input_result)
    def post(self):
        data = request.get_json(force=True)
        with session_scope() as session:
            return {'result': chatbot_input_repository.add_chatbot_input(session, data['email'], data['content'])}


chatbot_bp = Blueprint('chatbot', __name__)
api = Api(chatbot_bp, "/chatbot")
api.add_resource(GetChatInputRequest, "/getChatbotInputByUserEmail")
api.add_resource(AddChatInputRequest, "/addChatbotInput")
