from flask import Blueprint, render_template, redirect, url_for, flash, request
from app import db
from app.models import User
from werkzeug.security import generate_password_hash, check_password_hash
import re

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return redirect(url_for('main.signup'))

@main.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm_password']

        if password != confirm_password:
            flash('Passwords do not match.', 'error')
        elif len(password) < 8:
            flash('Password must be at least 8 characters long.', 'error')
        elif not re.search(r'[A-Z]', password):
            flash('Password must contain an uppercase letter.', 'error')
        elif not re.search(r'[a-z]', password):
            flash('Password must contain a lowercase letter.', 'error')
        elif not re.search(r'\d$', password):
            flash('Password must end with a number.', 'error')
        else:
            existing_user = User.query.filter_by(email=email).first()
            if existing_user:
                flash('Email address already in use.', 'error')
            else:
                new_user = User(first_name=first_name, last_name=last_name, email=email)
                new_user.set_password(password)
                db.session.add(new_user)
                db.session.commit()
                return redirect(url_for('main.thankyou'))

    return render_template('signup.html')

@main.route('/signin', methods=['GET', 'POST'])
def signin():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email=email).first()
        if user and user.check_password(password):
            return redirect(url_for('main.secretpage'))
        else:
            flash('Invalid email or password.', 'error')
    return render_template('signin.html')

@main.route('/secretpage')
def secretpage():
    return render_template('secretpage.html')

@main.route('/thankyou')
def thankyou():
    return render_template('thankyou.html')