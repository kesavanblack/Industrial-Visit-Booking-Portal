from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from models.db import db
from models.user import User
from models.student import Student

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        if current_user.role == 'student':
            return redirect(url_for('student.dashboard'))
        elif current_user.role == 'faculty':
            return redirect(url_for('faculty.dashboard'))
        elif current_user.role == 'admin':
            return redirect(url_for('admin.dashboard'))
        return redirect(url_for('index'))

    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        role = request.form.get('role') # User selects role: Admin, Faculty, Student

        user = User.query.filter_by(email=email, role=role).first()
        
        if user and user.check_password(password):
            login_user(user)
            flash(f'Logged in as {role.title()}', 'success')
            # Redirect based on role
            if role == 'student':
                return redirect(url_for('student.dashboard')) # To be implemented
            elif role == 'faculty':
                return redirect(url_for('faculty.dashboard')) # To be implemented
            elif role == 'admin':
                return redirect(url_for('admin.dashboard')) # To be implemented
            return redirect(url_for('index'))
        else:
            flash('Invalid email, password, or role selected', 'danger')

    return render_template('auth/login.html')

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    if request.method == 'POST':
        name = request.form.get('name')
        reg_no = request.form.get('register_number')
        dept = request.form.get('department')
        year = request.form.get('year')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')

        if password != confirm_password:
            flash('Passwords do not match!', 'danger')
            return redirect(url_for('auth.register'))

        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            flash('Email already registered!', 'warning')
            return redirect(url_for('auth.register'))

        # Create User
        new_user = User(email=email, role='student')
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit() # Commit to get ID

        # Create Student Profile
        new_student = Student(
            user_id=new_user.id,
            name=name,
            register_number=reg_no,
            department=dept,
            year=year
        )
        db.session.add(new_student)
        db.session.commit()

        flash('Registration successful! Please login.', 'success')
        return redirect(url_for('auth.login'))

    return render_template('auth/register.html')

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('auth.login'))
