from test_with_edozie import app, db, bcrypt
from flask import render_template, flash, request, redirect, url_for
from .forms import RegistrationForm, LoginForm, MathTestForm, PythonTestForm
from .models import Students, MathTest, TestAnswers, PythonTest, PythonTestAnswers
from flask_login import login_user, current_user, logout_user, login_required




@app.route('/')
def home():
    return render_template('home.html')


@app.route('/about')
def about():
    users = Students.query.all()
    return render_template('about.html', title='About')

@app.route('/feature')
def feature():
    return render_template('feature.html', title='Features')

@app.route('/register', methods=['GET', 'POST'])      
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        with app.app_context():
            db.create_all()
            student = Students(email=form.email.data, first_name=form.first_name.data, last_name=form.last_name.data,
                               gender=form.gender.data, password= bcrypt.generate_password_hash(form.password.data).decode('utf-8'))
            db.session.add(student)
            db.session.commit()
        flash('Your account has been created successfully', 'success')
        return redirect(url_for('home'))
    return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        student = Students.query.filter_by(email=form.email.data).first()
        if student and bcrypt.check_password_hash(student.password, form.password.data):
            login_user(student)
            return redirect(url_for('profile'))
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
                test_result = MathTest(question1=form.question1.data, question2=form.question2.data, question3=form.question3.data,
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
            student = MathTest.query.filter_by(student=current_user.id).all()[-1]
        except:
            return redirect(url_for('no_results_found'))
        answers = TestAnswers.query.filter_by(subject='Mathematics').first()
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
                test_result = PythonTest(question1=form.question1.data, question2=form.question2.data, question3=form.question3.data,
                               question4=form.question4.data, question5=form.question5.data, question6=form.question6.data,
                               question7=form.question7.data, question8=form.question8.data, question9=form.question9.data,
                               question10=form.question10.data, student=current_user.id)
        db.session.add(test_result)
        db.session.commit()
        flash('Your test have been successfully submitted', 'success')
        return redirect(url_for('profile'))
    return render_template('python_test.html', title='Python Test', form=form)


@login_required
@app.route('/check_python_results')
def check_python_results():
    with app.app_context():
        try:
            student = PythonTest.query.filter_by(student=current_user.id).all()[-1]
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
