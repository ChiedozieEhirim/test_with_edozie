import ssl 
import smtplib
from email.message import EmailMessage
from itsdangerous import URLSafeTimedSerializer
from test_with_edozie import app, db, email_password, email as email_sender
import random
from .models import OneTimePassword, Students
import threading


global secret_key
secret_key = app.config['SECRET_KEY']

def generate_confirmation_token(email):
    serializer = URLSafeTimedSerializer(secret_key)
    return serializer.dumps(email, salt=secret_key)


def confirm_token(token, expiration=3600):
    serializer = URLSafeTimedSerializer(secret_key)
    try:
        email = serializer.loads(token, salt=secret_key, max_age=expiration)
    except:
        return False
    return email
    



def generate_otp():
    otp = ''
    for i in range(6):
        otp += str(random.randint(1, 9))
    return otp

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

def send_otp_to_user(email):
    Subject = 'One time password for email verification'.title()
    otp_code = generate_otp()
    user = Students.query.filter_by(email=email).first()
    email_body = f'Hello, thanks for signing up. Please verify your email with \n OTP {otp_code}'
    with app.app_context():
        db.create_all()
        user_code = OneTimePassword(user=user.id, code=otp_code)
        db.session.add(user_code)
        db.session.commit()
    send_mail(email_receiver=email, email_subject=Subject, email_body=email_body)


def async_send_otp_to_user(email):
    email_send = threading.Thread(target=send_otp_to_user, args=(email, ))
    email_send.start()