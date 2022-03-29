from flask import Blueprint
from flask_restful import fields, Resource, marshal_with, reqparse, Api

from services.mail_sms import MailSender

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
        generate_code = args['content']
        content = """
            Hi,</br>
            You recently requested to rest the password for your %s account. Use the code below to proceed.
            </br></br>
            code: <strong>%s</strong>
            </br></br>
            If you did not request a password reset, please ignore this email. 
            This password reset code is only valid for the next 30 minutes.
            </br></br>
            Thanks,
            </br>
            FireApp 3.0 Team'
        """ % (args['email'], generate_code)
        MailSender().email(args['email'], args['subject'], content, args['sender'])
        return {"result": "ok"}


email_bp = Blueprint('email', __name__)
api = Api(email_bp, "/email")
api.add_resource(SendEmail, "/sendEmail")
