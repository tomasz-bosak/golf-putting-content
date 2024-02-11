from flask import Blueprint, render_template, request, flash, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash
auth = Blueprint('auth', __name__)
from .models import User
from . import db
from flask_login import login_user, login_required, logout_user, current_user

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        data = request.form
        print(data)
        email = request.form.get('email')
        password = request.form.get('password')
        
        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                flash('Login succesfully', category='success')
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else:
                flash('Incorrect password', category='error')
        else:
            flash('User unknown', category='error')
    return render_template("login.html", user=current_user)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

@auth.route('/sign-up', methods=['GET', 'POST'])
def sing_up():
    if request.method == 'POST':
        data = request.form
        print(data)
        email = request.form.get('email')
        firstName = request.form.get('firstName')
        password = request.form.get('password')
        password2 = request.form.get('password2')

        user = User.query.filter_by(email=email).first()
        if user:
            flash('Email already exists', category='error')
        elif len(email) < 4:
            flash('Email must be at least 4 characters', category='error')
        elif len(firstName) <2 :
            flash('Name must be at least 2 characters', category='error')
        elif password != password2:
            flash('Passwords does not match', category='error')
        elif len(password)<7:
            flash('Password is too short (min: 7 chars)', category='error')
        else:
            new_user = User(email=email, \
                            first_name=firstName, \
                            password = generate_password_hash(password, method='pbkdf2:sha256:1'))
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            flash('Account created', category='success')
            return redirect(url_for('views.home'))
        
    return render_template("sign_up.html", user=current_user)
