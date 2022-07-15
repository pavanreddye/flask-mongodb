import json
from app.templates import email_templates
from app.templates.email_templates import SendMail,sender_email

def send_email_notification(data):
    data = json.loads(data)
    subject = data['subject']
    message_string = email_templates.prepare_user_email(data['target_user_name'], data["login_id"], data["password"])
    to_email_id = data.get('target_email_id', 'pavane.py@gmail.com')
    cc_email_id = data.get('email_cc' ,None)
    SendMail(to_email_id, cc_email_id, subject, message_string ,sender_email)
    message = "Email Sent Successfully"
    status_code = 200
    return message, status_code
