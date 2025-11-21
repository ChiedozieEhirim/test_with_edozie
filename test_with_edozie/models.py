from test_with_edozie import login_manager, db, app
from flask_login import UserMixin
import datetime
from itsdangerous import URLSafeTimedSerializer as Serializer

@login_manager.user_loader
def load_user(user_id):
    return Students.query.get(int(user_id))

class Students(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(200), unique=True,  nullable=False, default='None')
    email = db.Column(db.String(100), unique=True, nullable=False)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    date_joined = datetime.datetime.utcnow()
    gender = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(300), nullable=False)
    is_verified = db.Column(db.Boolean, default=False)

    def __str__(self):
        return self.email

    def get_reset_token(self, expires_sec=1800):
        s = Serializer(app.config['SECRET_KEY'])
        return s.dumps({'user_id': self.id})
    
    @staticmethod
    def verify_reset_token(token, expires_sec=1800):
        s = Serializer(app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token, max_age=expires_sec)['user_id']
        except:
            return None
        return Students.query.get(user_id)


class OneTimePassword(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.Integer, nullable=False)
    user = db.Column(db.Integer, db.ForeignKey('students.id', ondelete='CASCADE'), nullable=False)



class MathTestAnswers(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    subject = db.Column(db.String(100), nullable=False)
    question1 = db.Column(db.String(100), nullable=False)
    question2 = db.Column(db.String(100), nullable=False)
    question3 = db.Column(db.String(100), nullable=False)
    question4 = db.Column(db.String(100), nullable=False)
    question5 = db.Column(db.String(100), nullable=False)
    question6 = db.Column(db.String(100), nullable=False)
    question7 = db.Column(db.String(100), nullable=False)
    question8 = db.Column(db.String(100), nullable=False)
    question9 = db.Column(db.String(100), nullable=False)
    question10 = db.Column(db.String(100), nullable=False)


class StudentMathResults(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    question1 = db.Column(db.String(100), nullable=False)
    question2 = db.Column(db.String(100), nullable=False)
    question3 = db.Column(db.String(100), nullable=False)
    question4 = db.Column(db.String(100), nullable=False)
    question5 = db.Column(db.String(100), nullable=False)
    question6 = db.Column(db.String(100), nullable=False)
    question7 = db.Column(db.String(100), nullable=False)
    question8 = db.Column(db.String(100), nullable=False)
    question9 = db.Column(db.String(100), nullable=False)
    question10 = db.Column(db.String(100), nullable=False)
    student = db.Column(db.Integer, db.ForeignKey('students.id'),  nullable=False)


class PythonTestAnswers(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    subject = db.Column(db.String(100), nullable=False)
    question1 = db.Column(db.String(100), nullable=False)
    question2 = db.Column(db.String(100), nullable=False)
    question3 = db.Column(db.String(100), nullable=False)
    question4 = db.Column(db.String(100), nullable=False)
    question5 = db.Column(db.String(100), nullable=False)
    question6 = db.Column(db.String(100), nullable=False)
    question7 = db.Column(db.String(100), nullable=False)
    question8 = db.Column(db.String(100), nullable=False)
    question9 = db.Column(db.String(100), nullable=False)
    question10 = db.Column(db.String(100), nullable=False)


class StudentPythonResults(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    question1 = db.Column(db.String(100), nullable=False)
    question2 = db.Column(db.String(100), nullable=False)
    question3 = db.Column(db.String(100), nullable=False)
    question4 = db.Column(db.String(100), nullable=False)
    question5 = db.Column(db.String(100), nullable=False)
    question6 = db.Column(db.String(100), nullable=False)
    question7 = db.Column(db.String(100), nullable=False)
    question8 = db.Column(db.String(100), nullable=False)
    question9 = db.Column(db.String(100), nullable=False)
    question10 = db.Column(db.String(100), nullable=False)
    student = db.Column(db.Integer, db.ForeignKey('students.id'), nullable=False)


class CryptographyTestAnswers(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    subject = db.Column(db.String(100), nullable=False)
    question1 = db.Column(db.String(100), nullable=False)
    question2 = db.Column(db.String(100), nullable=False)
    question3 = db.Column(db.String(100), nullable=False)
    question4 = db.Column(db.String(100), nullable=False)
    question5 = db.Column(db.String(100), nullable=False)
    question6 = db.Column(db.String(100), nullable=False)
    question7 = db.Column(db.String(100), nullable=False)
    question8 = db.Column(db.String(100), nullable=False)
    question9 = db.Column(db.String(100), nullable=False)
    question10 = db.Column(db.String(100), nullable=False)


class StudentCryptographyResults(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    question1 = db.Column(db.String(100), nullable=False)
    question2 = db.Column(db.String(100), nullable=False)
    question3 = db.Column(db.String(100), nullable=False)
    question4 = db.Column(db.String(100), nullable=False)
    question5 = db.Column(db.String(100), nullable=False)
    question6 = db.Column(db.String(100), nullable=False)
    question7 = db.Column(db.String(100), nullable=False)
    question8 = db.Column(db.String(100), nullable=False)
    question9 = db.Column(db.String(100), nullable=False)
    question10 = db.Column(db.String(100), nullable=False)
    student = db.Column(db.Integer, db.ForeignKey('students.id'), nullable=False)