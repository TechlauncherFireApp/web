from flask import Blueprint
from flask_restful import fields, Resource, marshal_with, reqparse, Api

from services import mail_sms

send_email_result = {
    "result": fields.String
}


class SendEmail(Resource):
    @marshal_with(send_email_result)
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument("email")
        parser.add_argument("subject")
        parser.add_argument("content")
        parser.add_argument("sender")
        args = parser.parse_args()
        mail_sms.MailSender().email(args['email'], args['subject'], args['content'], args['sender'])
        return {"result": "ok"}


email_bp = Blueprint('email', __name__)
api = Api(email_bp, "/email")
api.add_resource(SendEmail, "/sendEmail")
