from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from flask_migrate import Migrate
from flask_mail import Mail
from itsdangerous import URLSafeTimedSerializer
from dotenv import load_dotenv
import os

app = Flask(__name__)
load_dotenv()

app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
#app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://test_with_edozie_5smy_user:alWRdUwfdV305bi7urQ9eWX7sklqB5lo@dpg-d2ftu98gjchc73af3cc0-a.oregon-postgres.render.com/test_with_edozie_5smy'
db = SQLAlchemy(app)
migrate = Migrate(app, db)
bcrypt = Bcrypt(app)


login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'

app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.environ.get('EMAIL_HOST')
app.config['MAIL_PASSWORD'] = os.environ.get('EMAIL_PASSWORD')

email = os.environ.get('EMAIL_HOST')
email_password = os.environ.get('EMAIL_PASSWORD')

PAYSTACK_PRIVATE_KEY = os.environ.get('PAYSTACK_PRIVATE_KEY')
PAYSTACK_PUBLIC_KEY = os.environ.get('PAYSTACK_PUBLIC_KEY')

mail = Mail(app)

s = URLSafeTimedSerializer(app.config['SECRET_KEY'], )

from . import routes