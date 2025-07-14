from flask import Blueprint, render_template, redirect, request, url_for
from flask_login import login_required, current_user
from models import db, User, EmailRecord
from email_tracker import send_tracked_email

dashboard_bp = Blueprint('dashboard', __name__, url_prefix='/dashboard')

@dashboard_bp.route('/')
@login_required
def dashboard_home():
    users = User.query.filter_by(school_id=current_user.school_id).all()
    records = EmailRecord.query.filter_by(sender_id=current_user.id).all()
    return render_template('dashboard.html', users=users, records=records)

@dashboard_bp.route('/add_user', methods=['POST'])
@login_required
def add_user():
    name = request.form['name']
    email = request.form['email']
    password = request.form['password']
    new_user = User(name=name, email=email, password=password, school_id=current_user.school_id)
    db.session.add(new_user)
    db.session.commit()
    return redirect(url_for('dashboard.dashboard_home'))

@dashboard_bp.route('/send_email', methods=['POST'])
@login_required
def send_email():
    to_email = request.form['to_email']
    subject = request.form['subject']
    body = request.form['body']

    receiver = User.query.filter_by(email=to_email, school_id=current_user.school_id).first()
    if receiver:
        send_tracked_email(current_user, receiver, subject, body)
    return redirect(url_for('dashboard.dashboard_home'))
