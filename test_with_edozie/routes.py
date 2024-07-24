from test_with_edozie import app, db, bcrypt
from flask import render_template, flash, request, redirect, url_for
from .forms import RegistrationForm, LoginForm
from .models import Students
from flask_login import login_user, current_user, logout_user, login_required




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
    if current_user.is_authenticated:
        return redirect(url_for('home'))
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
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        student = Students.query.filter_by(email=form.email.data).first()
        input_password = form.password.data
        if student and bcrypt.check_password_hash(student.password, input_password.encode('utf-8')):
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

@login_required
@app.route('/subjects')
def subjects():
    return render_template('subjects.html')