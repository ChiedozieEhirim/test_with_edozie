from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt

app = Flask(__name__)

app.config['SECRET_KEY'] = 'Gtrytryterdytr6375865956eby5@$&*^&)(*UHIHBG*$R*&(&)(GBTHTE^U))'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://chiedozie:iyoIaNFY3E1KJNJnh6mOaN0lcZkCKH83@dpg-cqg0ufaju9rs73c69g80-a.oregon-postgres.render.com/teset_with_edozie_database'

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'

from . import routes

