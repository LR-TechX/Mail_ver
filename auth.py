from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_user, logout_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash
from models import db, User, School

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        school_name = request.form['school_name']
        email = request.form['email']
        name = request.form['name']
        password = generate_password_hash(request.form['password'], method='sha256')

        school = School(name=school_name, email=email)
        db.session.add(school)
        db.session.commit()

        user = User(email=email, name=name, password=password, is_super_admin=True, school_id=school.id)
        db.session.add(user)
        db.session.commit()
        login_user(user)
        return redirect(url_for('dashboard.dashboard_home'))

    return render_template('register.html')

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email=email).first()
        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for('dashboard.dashboard_home'))
        flash('Invalid credentials')
    return render_template('login.html')

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))
