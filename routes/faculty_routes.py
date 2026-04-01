from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from models.db import db
from models.visit import Visit
from models.booking import Booking
from werkzeug.utils import secure_filename
import os

faculty_bp = Blueprint('faculty', __name__, url_prefix='/faculty')

def faculty_required(f):
    from functools import wraps
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or current_user.role != 'faculty':
            flash('Access denied.', 'danger')
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function

@faculty_bp.route('/dashboard')
@login_required
@faculty_required
def dashboard():
    faculty = current_user.faculty_profile
    # Visits assigned to this faculty
    assigned_visits = Visit.query.filter_by(faculty_id=faculty.id).all()
    
    visit_ids = [v.id for v in assigned_visits]
    pending_approvals = Booking.query.filter(Booking.visit_id.in_(visit_ids), Booking.status == 'Pending').count()
    
    return render_template('faculty/dashboard.html', 
                           faculty=faculty, 
                           assigned_visits=assigned_visits,
                           pending_approvals=pending_approvals)

@faculty_bp.route('/approve/<int:visit_id>', methods=['GET', 'POST'])
@login_required
@faculty_required
def approve_students(visit_id):
    visit = Visit.query.get_or_404(visit_id)
    if visit.faculty_id != current_user.faculty_profile.id:
        flash('You are not authorized to manage this visit.', 'danger')
        return redirect(url_for('faculty.dashboard'))

    bookings = Booking.query.filter_by(visit_id=visit.id).all() # Show all to manage

    if request.method == 'POST':
        booking_id = request.form.get('booking_id')
        action = request.form.get('action')
        
        booking = Booking.query.get(booking_id)
        if booking and action == 'approve':
            booking.status = 'Approved'
            flash(f'Student {booking.student_profile.name} approved.', 'success')
        elif booking and action == 'reject':
            booking.status = 'Rejected'
            # Restore seat if rejected?
            # visit.available_seats += 1
            flash(f'Student {booking.student_profile.name} rejected.', 'warning')
            
        db.session.commit()
        return redirect(url_for('faculty.approve_students', visit_id=visit.id))

    return render_template('faculty/approve_students.html', visit=visit, bookings=bookings)

@faculty_bp.route('/attendance')
@login_required
@faculty_required
def attendance():
    return render_template('faculty/qr_attendance.html')

@faculty_bp.route('/upload_report', methods=['GET', 'POST'])
@login_required
@faculty_required
def upload_report():
    if request.method == 'POST':
        # File upload logic
        if 'report' not in request.files:
            flash('No file part', 'danger')
            return redirect(request.url)
        
        file = request.files['report']
        if file.filename == '':
            flash('No selected file', 'danger')
            return redirect(request.url)

        if file:
            filename = secure_filename(file.filename)
            # Save to uploads/reports
            # file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            flash('Report uploaded successfully (Simulated).', 'success')
            return redirect(url_for('faculty.dashboard'))
            
    return render_template('faculty/upload_report.html')
