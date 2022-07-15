import sys
import smtplib
from email.mime.text import MIMEText

SMTPRelayHost1 = 'smtp.gmail.com'
sender_email = "pavane.py@gmail.com"

def SendMail(email_to,email_cc,Subject,msgString,sender_email):
    """
    Send mail to distribution list
    :param Email_TO_DL: email list
    :param Subject: mail subject
    :param msgString: mail body
    """
    #try:
    SMTPRelayHost=SMTPRelayHost1
    FromEmailId=sender_email
    sys.stdout.flush()
    s = smtplib.SMTP(host=SMTPRelayHost)
    msg = MIMEText(msgString,'html')
    msg['Subject'] = Subject
    msg['From'] = FromEmailId
    msg['To'] = email_to

    if email_cc !="None":
        msg['Cc']=email_cc
    to_list = [email_to, email_cc]
    s.sendmail(FromEmailId,to_list, msg.as_string())
    s.quit()



def prepare_user_email(target_user_name, login_id, password):
    return """
    <p>Dear  """ + str(target_user_name) + """,</p>
    <p>An account has been created for you in Madapalli Development Foundation Committe. Please find your credentials below</p>
    <p>Login ID&nbsp; &nbsp; &nbsp; -  """ + str(login_id) + """</p>
    <p>Password&nbsp; &nbsp;-  """ + str(password) + """</p>
    <p>This is only a temporary password. Kindly reset your password after your first login</p>
    <p>You can access MPDFC <a href="'""" + """'">here&nbsp;</a></p>
    <p>&nbsp;</p>
    <p>Kind regards</p>
    <p><span style="color: #0000ff;">MPDFC Team</span></p>

    """
