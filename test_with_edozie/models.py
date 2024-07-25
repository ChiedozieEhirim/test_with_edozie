from test_with_edozie import login_manager, db, app
from flask_login import UserMixin
import datetime
from itsdangerous import URLSafeTimedSerializer as serializer

@login_manager.user_loader
def load_user(user_id):
    return Students.query.get(int(user_id))

class Students(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True, nullable=False)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    date_joined = datetime.datetime.utcnow()
    gender = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(300), nullable=False)
    is_active = True

    def get_reset_token(self, expires_sec=1800):
        s = serializer(app.config['SECRET_KEY'],expires_sec)
        return s.dumps({'user_id':self.id}).decode('utf-8')

    @staticmethod
    def verify_reset_token(token):
        s = serializer(app.config['SECRET_KEY'])
        try:
            s.loads(token)['user_id']
        except:
            return None
        return Students.query.get(int(id))
    

class MathTest(db.Model):
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


class TestAnswers(db.Model):
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