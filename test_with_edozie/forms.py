
import flask_wtf
from wtforms import StringField, EmailField, RadioField, PasswordField, SubmitField
from wtforms.validators import Email, InputRequired, Length, EqualTo


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