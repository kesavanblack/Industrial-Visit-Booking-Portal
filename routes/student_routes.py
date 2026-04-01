from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from models.db import db
from models.visit import Visit
from models.booking import Booking
from models.payment import Payment
from datetime import datetime

student_bp = Blueprint('student', __name__, url_prefix='/student')

def student_required(f):
    from functools import wraps
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or current_user.role != 'student':
            flash('Access denied.', 'danger')
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function

@student_bp.route('/dashboard')
@login_required
@student_required
def dashboard():
    # Get student profile
    student = current_user.student_profile
    my_bookings = Booking.query.filter_by(student_id=student.id).all()
    
    total_applied = len(my_bookings)
    approved_count = sum(1 for b in my_bookings if b.status == 'Approved')
    pending_count = sum(1 for b in my_bookings if b.status == 'Pending')
    
    return render_template('student/dashboard.html', 
                           student=student,
                           total_applied=total_applied, 
                           approved_count=approved_count, 
                           pending_count=pending_count)

@student_bp.route('/visits')
@login_required
@student_required
def view_visits():
    # Only show upcoming visits
    visits = Visit.query.filter(Visit.visit_date >= datetime.today().date()).all()
    return render_template('student/view_visits.html', visits=visits)

@student_bp.route('/book/<int:visit_id>', methods=['GET', 'POST'])
@login_required
@student_required
def book_visit(visit_id):
    visit = Visit.query.get_or_404(visit_id)
    student = current_user.student_profile
    
    # Check if already booked
    existing_booking = Booking.query.filter_by(student_id=student.id, visit_id=visit.id).first()
    if existing_booking:
        flash('You have already applied for this visit.', 'warning')
        return redirect(url_for('student.view_bookings'))

    if request.method == 'POST':
        if visit.available_seats > 0:
            # Create booking
            new_booking = Booking(
                student_id=student.id,
                visit_id=visit.id,
                status='Pending'
            )
            # Decrease seats logic could be here or after approval. 
            # Usually seats are locked on payment or approval. 
            # Requirement says "Seat auto-lock logic". Let's lock it temporarily or decrease.
            # Decreasing now implies "First Come First Serve" application.
            visit.available_seats -= 1
            
            db.session.add(new_booking)
            db.session.commit()
            
            flash('Booking application submitted successfully!', 'success')
            return redirect(url_for('student.view_bookings'))
        else:
            flash('Sorry, no seats available.', 'danger')
            
    return render_template('student/book_visit.html', visit=visit, student=student)

@student_bp.route('/my_bookings')
@login_required
@student_required
def view_bookings():
    student = current_user.student_profile
    bookings = Booking.query.filter_by(student_id=student.id).order_by(Booking.booking_date.desc()).all()
    return render_template('student/status.html', bookings=bookings)

@student_bp.route('/payment/<int:booking_id>', methods=['GET', 'POST'])
@login_required
@student_required
def payment(booking_id):
    booking = Booking.query.get_or_404(booking_id)
    
    # Only allow payment if Approved (or if user design allows pre-payment)
    # Usually Approval -> Payment -> Confirmed.
    
    if request.method == 'POST':
        amount = float(request.form.get('amount'))
        # Simulate payment
        new_payment = Payment(
            booking_id=booking.id,
            amount=amount,
            transaction_id=f"TXN-{datetime.now().timestamp()}",
            status='Success'
        )
        booking.payment_status = 'Paid'
        booking.status = 'Confirmed' # Auto confirm after payment
        
        db.session.add(new_payment)
        db.session.commit()
        
        flash('Payment Successful! Visit Confirmed.', 'success')
        return redirect(url_for('student.view_bookings'))
        
    return render_template('student/payment.html', booking=booking)
