from test_with_edozie import app, db, bcrypt, mail, s 
from flask import render_template, flash, request, redirect, url_for, jsonify
from .forms import RegistrationForm, EmailVerificationForm, LoginForm, MathTestForm, PythonTestForm, CryptographyTestForm, \
    PasswordResetRequestForm, ResetPasswordForm
from .models import Students, OneTimePassword, StudentMathResults, MathTestAnswers, StudentPythonResults, PythonTestAnswers, \
        StudentCryptographyResults, CryptographyTestAnswers
from flask_login import login_user, current_user, logout_user, login_required
import itsdangerous
from .utils import send_mail, email_sender, email_password, async_send_otp_to_user
import requests
import re
from bs4 import BeautifulSoup


@app.route('/')
def home():
    return render_template('home.html')

@app.route('/about')
def about():
    with app.app_context():
        student = Students.query.filter_by(email='ehirimchiedozie@outlook.com').first()
        db.session.delete(student)
        db.session.commit()
    return render_template('about.html', title='About')

@app.route('/feature')
def feature():
    return render_template('feature.html', title='Features')

@app.route('/courses')
def courses():
    return render_template('courses.html', title='Our Courses')

@app.route('/register', methods=['GET', 'POST'])      
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        with app.app_context():
            db.create_all()
            student = Students(
                               username=form.username.data,
                               email=form.email.data,
                               first_name=form.first_name.data,
                               last_name=form.last_name.data,
                               gender=form.gender.data,
                               password= bcrypt.generate_password_hash(form.password.data).decode('utf-8')
                               )
            db.session.add(student)
            db.session.commit()
            flash(f'An OTP has been sent to {form.email.data}. Use it to verify your account','info')
            async_send_otp_to_user(email=form.email.data)
            return redirect('confirm_email')
    return render_template('register.html', form=form) 


@app.route('/confirm_email', methods=['GET', 'POST'])
def confirm_email():
    form = EmailVerificationForm()
    if form.validate_on_submit():
        try:
            otp_code = form.code.data
            user_code_obj = OneTimePassword.query.filter_by(code=otp_code).first()
            user = Students.query.filter_by(id=user_code_obj.user).first()
            if not user.is_verified:
                user.is_verified = True
                db.session.commit()
                flash('Your account has been verified successfully', 'success')
                return redirect(url_for('login'))
            else:
                flash('Invalid OTP', 'error')
        except AttributeError as e:
           flash('This OTP is invalid'.title(), 'error')
    return render_template('confirm_email.html', title='Email Verification', form=form)


# @app.route('/confirm_email/<token>')
# def confirm_email(token):
#     try:
#         email = s.loads(token, salt='email-confirm')
#     except(itsdangerous.SignatureExpired, itsdangerous.BadTimeSignature) as error:
#         if str(error).endswith('seconds'):
#             error_message = 'This token has expired. Please try again'
#         elif str(error).endwith('does not match'):
#             error_message = 'This token is invalid. Please check and try again'
#         return error_message
#     else:
#         owner_email = request.form.get('email')
#         owner = Students.query.filter_by(email=owner_email).first()
#         owner.confirmed = True
#         db.session.commit()
#     return '''<h1>Registration was successful</h1>'''



@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        student = Students.query.filter_by(email=form.email.data).first()
        if student and bcrypt.check_password_hash(student.password, form.password.data) and student.is_verified==True:
            login_user(student)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('profile'))
        else:
            flash('Login Unsuccessful. Check your email and password and try again')
    return render_template('login.html', form=form)

@login_required
@app.route('/confirm_logout')
def confirm_logout():
    return render_template('confirm_logout.html')

@login_required
@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))

@login_required
@app.route('/profile')
def profile():
    return render_template('profile.html')



@app.route('/reset_password_request', methods=['GET', 'POST'])
def reset_password_request():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = PasswordResetRequestForm()
    if form.validate_on_submit():
        student = Students.query.filter_by(email=form.email.data).first()
        if student:
            email_subject = 'Change your password'.title()
            token = student.get_reset_token()
            email_body = f'''To reset your password, please follow the link below
            {url_for('reset_token', token=token, _external=True)}
            '''
            send_mail(student.email, email_subject, email_body)
            flash("A message has been sent to your mail with information on how to reset your password", 'success')
            return redirect(url_for('login'))
    return render_template('reset_password_request.html', form=form)


@app.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    student = Students.verify_reset_token(token)
    if student is None:
        flash('Token is invalid or expired. Please try again', 'warning')
        return redirect(url_for('reset_password_request'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        student.password = hashed_password
        db.session.commit()
        flash('Password change was successful')
        return redirect(url_for('login'))
    return render_template('reset_password.html', form=form)

@login_required
@app.route('/subjects')
def subjects():
    return render_template('subjects.html')



@login_required
@app.route('/math_test', methods=['GET', 'POST'])
def math_test():
    form = MathTestForm()
    if form.validate_on_submit():
        with app.app_context():
                db.create_all()
                test_result = StudentMathResults(question1=form.question1.data, question2=form.question2.data, question3=form.question3.data,
                               question4=form.question4.data, question5=form.question5.data, question6=form.question6.data,
                               question7=form.question7.data, question8=form.question8.data, question9=form.question9.data,
                               question10=form.question10.data, student=current_user.id)
        db.session.add(test_result)
        db.session.commit()
        flash('Your test have been successfully submitted', 'success')
        return redirect(url_for('profile'))
    return render_template('math_test.html', title='Math Test', form=form)



@login_required
@app.route('/check_results')
def check_results():
    return render_template('check_results.html')


@login_required
@app.route('/check_maths_results')
def check_math_results():
    with app.app_context():
        try:
            student = StudentMathResults.query.filter_by(student=current_user.id).all()[-1]
        except:
            return redirect(url_for('no_results_found'))
        answers = MathTestAnswers.query.filter_by(subject='Basic Maths').first()
        student_answers = [
            student.question1, student.question2, student.question3, student.question4, student.question5,
            student.question6, student.question7, student.question8, student.question9, student.question10
        ]
        correct_answers = [
            answers.question1, answers.question2, answers.question3, answers.question4, answers.question5,
            answers.question6, answers.question7, answers.question8, answers.question9, answers.question10
        ]

        count = 0
        mark = 0
        while count < 10:
            if student_answers[count] == correct_answers[count]:
                mark += 1
            else:
                pass
            count += 1
        total_score = mark
        
    return render_template('check_math_results.html', title='Math Results', total_score=total_score)

@login_required
@app.route('/no_results_found')
def no_results_found():
    return render_template('no_results_found.html', title='No Resuts Found')


@login_required
@app.route('/python_test', methods=['GET', 'POST'])
def python_test():
    form = PythonTestForm()
    if form.validate_on_submit():
        with app.app_context():
                db.create_all()
                test_result = StudentPythonResults(question1=form.question1.data, question2=form.question2.data, question3=form.question3.data,
                               question4=form.question4.data, question5=form.question5.data, question6=form.question6.data,
                               question7=form.question7.data, question8=form.question8.data, question9=form.question9.data,
                               question10=form.question10.data, student=current_user.id)
    return render_template('python_test.html', title='Python Test', form=form)
                       
                       

@login_required
@app.route('/check_python_results')
def check_python_results():
    with app.app_context():
        try:
            student = StudentPythonResults.query.filter_by(student=current_user.id).all()[-1]
        except:
            return redirect(url_for('no_results_found'))
        answers = PythonTestAnswers.query.filter_by(subject='Basic Python').first()
        student_answers = [
            student.question1, student.question2, student.question3, student.question4, student.question5,
            student.question6, student.question7, student.question8, student.question9, student.question10
        ]
        correct_answers = [
            answers.question1, answers.question2, answers.question3, answers.question4, answers.question5,
            answers.question6, answers.question7, answers.question8, answers.question9, answers.question10
        ]
        count = 0
        mark = 0
        while count < 10:
            if student_answers[count] == correct_answers[count]:
                mark += 1
            else:
                pass
            count += 1
        total_score = mark
        
    return render_template('check_python_results.html', title='Python Results', total_score=total_score)


@login_required
@app.route('/cryptography_test', methods=['GET', 'POST'])
def cryptography_test():
    form = CryptographyTestForm()
    if form.validate_on_submit():
        with app.app_context():
                db.create_all()
                test_result = StudentCryptographyResults(question1=form.question1.data, question2=form.question2.data, question3=form.question3.data,
                               question4=form.question4.data, question5=form.question5.data, question6=form.question6.data,
                               question7=form.question7.data, question8=form.question8.data, question9=form.question9.data,
                               question10=form.question10.data, student=current_user.id)
        db.session.add(test_result)
        db.session.commit()
        flash('Your test have been successfully submitted', 'success')
        return redirect(url_for('profile'))
    return render_template('cryptography_test.html', form=form)


@login_required
@app.route('/check_basic_cryptography_results')
def check_basic_cryptography_results():
    with app.app_context():
        try:
            student = StudentCryptographyResults.query.filter_by(student=current_user.id).all()[-1]
        except:
            return redirect(url_for('no_results_found'))
        answers = StudentCryptographyResults.query.all()[0]
        student_answers = [
            student.question1, student.question2, student.question3, student.question4, student.question5,
            student.question6, student.question7, student.question8, student.question9, student.question10
        ]
        correct_answers = [
            answers.question1, answers.question2, answers.question3, answers.question4, answers.question5,
            answers.question6, answers.question7, answers.question8, answers.question9, answers.question10
        ]
        count = 0
        mark = 0
        while count < 10:
            if student_answers[count] == correct_answers[count]:
                mark += 1
            else:
                pass
            count += 1
        total_score = mark
        
    return render_template('check_basic_cryptography_results.html', title='basic_cryptography'.capitalize(), total_score=total_score)


@app.route('/get_ip')
def get_ip():
    response = requests.get('https://dnsleaktest.com').text
    soup = BeautifulSoup(response, 'lxml')
    welcome_address = soup.find('div', class_='welcome')
    element_texts = [i.text for i in  welcome_address]
    ip_element = element_texts[1]
    location_element = element_texts[3]
    ip = re.findall(r'\d+.\d+.\d+.\d+', ip_element)
    ip_address = ip[0]
    location = location_element.replace('from ', '')
    return render_template('ip_address.html', title='Ip Address', ip_address=ip_address, location=location)