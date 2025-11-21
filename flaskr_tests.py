import ssl
import smtplib
from email.message import EmailMessage

global email_sender
global email_password

email_sender = 'chiedoziedavidehirim@gmail.com'
email_password = 'ogeapajgdeybegnu'

def send_mail(email_receiver, email_subject, email_body):
    em = EmailMessage()
    em['From'] = email_sender
    em['To'] = email_receiver
    em['Subject'] = email_subject
    em.set_content(email_body)

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL('smtp.gmail.com',465,context=context) as smtp:
        smtp.login(email_sender, email_password)
        smtp.sendmail(email_sender, [email_receiver], em.as_string())


send_mail('ehirimchiedozie96@yahoo.com', 'Confirm Email', 'Hi, keep pushing, you will make it')