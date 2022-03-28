import base64
import os
from datetime import datetime

from sendgrid import SendGridAPIClient, FileContent, FileType, FileName, Disposition, ContentId, Attachment
from sendgrid.helpers.mail import Mail

from services.attachment import AttachmentService
from services.secrets import SecretService

secret = SecretService(f"email/{os.environ.get('env', 'dev')}/api")
attachment = AttachmentService()


class MailSender:
    api_key = None
    from_email = None

    templates = {
        'roster': 'd-000f5ba606324814b0cf316d98ffb59f'
    }

    def __init__(self, **kwargs):
        self.api_key = secret.get()['api_key']
        self.from_email = kwargs.get('from_email', secret.get()['from_email'])

    def email(self, to_email, template, data, start_time, end_time):
        # We always append on the destination url to help.
        data['url'] = secret.get()['url']

        # Build the mail object & send the email.
        message = Mail(
            from_email=self.from_email,
            to_emails=to_email,
            html_content='<strong>This will be replaced by your template.</strong>')
        message.dynamic_template_data = data
        message.template_id = self.templates[template]

        if template == 'roster':
            ics = attachment.generate('Shift Assignment', start_time, end_time)
            message.add_attachment(
                Attachment(
                    file_content=base64.b64encode(str(ics).encode('utf-8')).decode(),
                    file_name='shift.ics',
                    file_type='text/calendar',
                    disposition='attachment'
                ))

        try:
            sendgrid_client = SendGridAPIClient(api_key=self.api_key)
            response = sendgrid_client.send(message)
            print(response.status_code)
            print(response.body)
            print(response.headers)
        except Exception as e:
            print(e)

    def email1(self, to_email, subject, html_context):
        message = Mail(
            from_email='bujue.why@gmail.com',
            to_emails=to_email,
            subject=subject,
            html_content=html_context)
        try:
            sg = SendGridAPIClient('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')
            response = sg.send(message)
            print(response.status_code)
            print(response.body)
            print(response.headers)
        except Exception as e:
            print(e.message)


#sender = MailSender()
#sender.email(['u6797866@anu.edu.au'], 'roster', {
#    'startTime': datetime.now().strftime('%H:%M:%S %d %b %Y'),
#    'endTime': datetime.now().strftime('%H:%M:%S %d %b %Y'),
#    'role': 'Driver',
#    'url': "https://test.com"
#}, datetime.now(), datetime.now())
