from flask import Flask, render_template, redirect, flash, url_for, request
import flask_wtf
from wtforms import StringField, EmailField, RadioField, PasswordField, SubmitField
from wtforms.validators import Email, InputRequired, Length, EqualTo
from flask_sqlalchemy import SQLAlchemy
import datetime
from itsdangerous import URLSafeTimedSerializer as serializer
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, login_user, current_user, UserMixin, logout_user, login_required


app = Flask(__name__)

app.config['SECRET_KEY'] = 'Gtrytryterdytr6375865956eby5@$&*^&)(*UHIHBG*$R*&(&)(GBTHTE^U))'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'

class RegistrationForm(flask_wtf.FlaskForm):
    email = EmailField(label='Email Address', validators=[Email()])
    first_name = StringField(label='First Name', validators=[InputRequired(),Length(min=2, max=100)])
    last_name = StringField(label='Last Name', validators=[InputRequired(),Length(min=2, max=100)])
    gender = RadioField('Gender', choices=[('Male', 'Male'), ('Female', 'Female')])
    password = PasswordField(label='Password', validators=[InputRequired(), Length(min=8, max=20)])
    confirm_password = PasswordField(label='Enter the same password for confirmation', validators=[InputRequired(), EqualTo('password')])
    submit = SubmitField('Register')


class LoginForm(flask_wtf.FlaskForm):
    email = EmailField(label='Email Address', validators=[Email()])    
    password = PasswordField(label='Password', validators=[InputRequired(), Length(min=8, max=20)])
    submit = SubmitField('Login')

    

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

@app.route('/')
def home():
    return render_template('home.html')


@app.route('/about')
def about():
    return render_template('about.html', title='About')

@app.route('/feature')
def feature():
    return render_template('feature.html', title='Features')

@app.route('/register', methods=['GET', 'POST'])      
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        with app.app_context():
            db.create_all()
            student = Students(email=form.email.data, first_name=form.first_name.data, last_name=form.last_name.data,
                               gender=form.gender.data, password= bcrypt.generate_password_hash(form.password.data))
            db.session.add(student)
            db.session.commit()
        flash('Your account has been created successfully', 'success')
        return redirect(url_for('home'))
    return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        student = Students.query.filter_by(email=form.email.data).first()
        if student and bcrypt.check_password_hash(student.password, form.password.data):
            login_user(student)
            redirect(url_for('profile'))
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('profile'))
        else:
            flash('Login Unsuccessfull. Check your email and password and try again')
    return render_template('login.html', form=form)

@login_required
@app.route('/confirm_logout')
def confirm_logout():
    return render_template('confirm_logout.html')

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))

@login_required
@app.route('/profile')
def profile():
    return render_template('profile.html')


if __name__ == '__main__':
    app.run(debug=True)