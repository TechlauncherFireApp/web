import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

from services.secrets import SecretService

secret = SecretService(f"email/{os.environ.get('env', 'dev')}/api")


class MailSender:
    api_key = None
    from_email = None

    templates = {
        'roster': 'd-000f5ba606324814b0cf316d98ffb59f'
    }

    def __init__(self, **kwargs):
        self.api_key = secret.get()['api_key']
        self.from_email = kwargs.get('from_email', secret.get()['from_email'])

    def email(self, to_email, template, data):
        # We always append on the destination url to help.
        data['url'] = secret.get()['url']

        # Build the mail object & send the email.
        message = Mail(
            from_email=self.from_email,
            to_emails=to_email,
            html_content='<strong>This will be replaced by your template.</strong>')
        message.dynamic_template_data = data
        message.template_id = self.templates[template]
        try:
            sendgrid_client = SendGridAPIClient(api_key=self.api_key)
            response = sendgrid_client.send(message)
            print(response.status_code)
            print(response.body)
            print(response.headers)
        except Exception as e:
            print(e)


#
# sender.email(['u6797866@anu.edu.au'], 'roster', {
#     'startTime': '11:30am 4 Apr 2020',
#     'endTime': '11:30am 4 Apr 2020',
#     'role': 'Driver',
#     'url': "https://test.com"
# })
