import smtplib
import ssl
from email.message import EmailMessage

email_sender = 'chiedoziedavidehirim@gmail.com'
email_receiver = 'ehirimchiedozie96@yahoo.com'
email_password = 'ogeapajgdeybegnu'
email_subject = 'I Got To Live'
email_body = '''
I hope I don't go before its my time
Before I can show what I'll do with my life
My wife will be sad and keep asking why
My Mom will be mad 'cause that's just what's she's like
But I hope that someone remembers me well
That my messed up stories are good ones to tell
Don't get to decide, but if I did
I wouldn't die before I got to live
'''

em = EmailMessage()
em['From'] = email_sender
em['To'] = email_receiver
em['Subject'] = email_subject
em.set_content(email_body)

context = ssl.create_default_context()
with smtplib.SMTP_SSL('smtp.gmail.com',465,context=context) as smtp:
    smtp.login(email_sender, email_password)
    smtp.sendmail(email_sender, email_receiver, em.as_string())