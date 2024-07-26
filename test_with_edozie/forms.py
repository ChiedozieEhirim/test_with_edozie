import flask_wtf
from wtforms import StringField, EmailField, RadioField, PasswordField, SubmitField
from wtforms.validators import Email, InputRequired, Length, EqualTo, ValidationError
from .models import Students

class RegistrationForm(flask_wtf.FlaskForm):
    email = EmailField(label='Email Address', validators=[Email()])
    first_name = StringField(label='First Name', validators=[InputRequired(),Length(min=2, max=100)])
    last_name = StringField(label='Last Name', validators=[InputRequired(),Length(min=2, max=100)])
    gender = RadioField('Gender', choices=[('Male', 'Male'), ('Female', 'Female')])
    password = PasswordField(label='Password', validators=[InputRequired(), Length(min=8, max=20)])
    confirm_password = PasswordField(label='Enter the same password for confirmation', validators=[InputRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_email(self, email):
        student = Students.query.filter_by(email=email.data).first()
        if student:
            raise ValidationError('Email already exists. Please use a different one')



class LoginForm(flask_wtf.FlaskForm):
    email = EmailField(label='Email Address', validators=[Email()])    
    password = PasswordField(label='Password', validators=[InputRequired(), Length(min=8, max=20)])
    submit = SubmitField('Login')


class MathTestForm(flask_wtf.FlaskForm):
    question1 = RadioField(choices=[('30', '30'), ('40', '40'), ('50', '50')])
    question2 = RadioField(choices=[('23', '23'), ('20', '20'), ('21', '21')])
    question3 = RadioField(choices=[('tan2A', 'tan2A'), ('cos2A', 'cos2A'), ('sin2A', 'sin2A')])
    question4 = RadioField(choices=[('(x-5)(x-2)', '(x-5)(x-2)'), ('(x+5)(x+2)', '(x+5)(x+2)'), ('(x+5)(x-2)', '(x+5)(x-2)')])
    question5 = RadioField(choices=[('2010', '2010'), ('2012', '2012'), ('2018', '2018')])
    question6 = RadioField(choices=[('45', '45'), ('50', '50'), ('55', '55')])
    question7 = RadioField(choices=[('Opposite', 'Opposite'), ('Hypotenuse', 'Hypotenuse'), ('Adjacent', 'Adjacent')])
    question8 = RadioField(choices=[('Modulus', 'Modulus'), ('Argument', 'Argument'), ('Correspondence', 'Correspondence')])
    question9 = RadioField(choices=[('4', '4'), ('5', '5'), ('6', '6')])
    question10 = RadioField(choices=[('arctan(3/4)', 'arctan(3/4)'), ('arctan(4/3)', 'arctan(4/3)'), ('arcsin(3/4)', 'arcsin(3/4)')])
    submit = SubmitField('Submit')


class PythonTestForm(flask_wtf.FlaskForm):
    question1 = RadioField(choices=[('List', 'List'), ('String', 'String'),('Tuple', 'Tuple')])
    question2 = RadioField(choices=[('variable_name=variable_value', 'variable_name=variable_value'),
    ('variable_value=variable_name', 'variable_value=variable_name'),
    ('None of the above', 'None of the above')])
    question3 = RadioField(choices=[('Condensation', 'Condensation'),('Combination', 'Combination'), ('Concatenation', 'Concatenation')])
    question4 = RadioField(choices=[('print(a)', 'print(a)'), ('Print(a)',  'Print(a)'), ('print(A)', 'print(A)')])
    question5 = RadioField(choices=[('True', 'True'), ('False', 'False')])
    question6 = RadioField(choices=[('//', '//'), ('#', '#'), ('%', '%')])
    question7 = RadioField(choices=[('Triple Quotes', 'Triple Quotes'),('Double Quotes', 'Double Quotes'), ('Single Quotes', 'Single Quotes')])
    question8 = RadioField(choices=[('3name', '3name'), ('name 3', 'name 3'), ('name3', 'name3')])
    question9 = RadioField(choices=[('Hyphen(-)', 'Hyphen(-)'),
    ('Semicolon(;)', 'Semicolon(;)'),
    ('Underscore(_)', 'Underscore(_)')])
    question10 = RadioField(choices=[('Each word excepts the first starts with a capital letter', 'Each word excepts the first starts with a capital letter'),
    ('Each word starts with a capital letter', 'Each word starts with a capital letter'),
    ('All the words are separated by an underscore', 'All the words are separated by an underscore') ])
    submit = SubmitField('Submit')

