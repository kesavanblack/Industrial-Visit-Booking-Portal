from flask import Blueprint, render_template, request, redirect, url_for, flash, make_response
from flask_login import login_required, current_user
import csv
import io
from reportlab.pdfgen import canvas
from models.db import db
from models.industry import Industry
from models.visit import Visit
from models.faculty import Faculty
from models.user import User
from models.student import Student
from models.payment import Payment
from models.feedback import Feedback
from datetime import datetime

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

# Decorator to ensure admin access (simplified)
def admin_required(f):
    from functools import wraps
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or current_user.role != 'admin':
            flash('You do not have permission to access this page.', 'danger')
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function

@admin_bp.route('/dashboard')
@login_required
@admin_required
def dashboard():
    # Fetch stats
    total_industries = Industry.query.count()
    total_visits = Visit.query.count()
    # Placeholder stats
    total_students = 120 
    return render_template('admin/dashboard.html', 
                           total_industries=total_industries,
                           total_visits=total_visits,
                           total_students=total_students)

@admin_bp.route('/add_industry', methods=['GET', 'POST'])
@login_required
@admin_required
def add_industry():
    if request.method == 'POST':
        name = request.form.get('name')
        location = request.form.get('location')
        contact_person = request.form.get('contact_person')
        email = request.form.get('email')
        phone = request.form.get('phone')
        
        new_industry = Industry(name=name, location=location, contact_person=contact_person, email=email, phone=phone)
        db.session.add(new_industry)
        db.session.commit()
        flash('Industry added successfully!', 'success')
        return redirect(url_for('admin.dashboard'))
        
    return render_template('admin/add_industry.html')

@admin_bp.route('/create_visit', methods=['GET', 'POST'])
@login_required
@admin_required
def create_visit():
    industries = Industry.query.all()
    faculties = Faculty.query.all()
    
    if request.method == 'POST':
        industry_id = request.form.get('industry')
        title = request.form.get('title')
        description = request.form.get('description')
        visit_date_str = request.form.get('visit_date')
        fee = request.form.get('fee')
        total_seats = request.form.get('total_seats')
        faculty_id = request.form.get('faculty')
        
        visit_date = datetime.strptime(visit_date_str, '%Y-%m-%d').date()
        
        new_visit = Visit(
            industry_id=industry_id,
            title=title,
            description=description,
            visit_date=visit_date,
            fee=float(fee),
            total_seats=int(total_seats),
            available_seats=int(total_seats),
            faculty_id=faculty_id
        )
        db.session.add(new_visit)
        db.session.commit()
        flash('Industrial Visit Created Successfully!', 'success')
        return redirect(url_for('admin.dashboard'))

    return render_template('admin/create_visit.html', industries=industries, faculties=faculties)

@admin_bp.route('/analytics')
@login_required
@admin_required
def analytics():
    return render_template('admin/analytics.html')

@admin_bp.route('/reports')
@login_required
@admin_required
def reports():
    return render_template('admin/reports.html')

@admin_bp.route('/manage_faculty')
@login_required
@admin_required
def manage_faculty():
    faculty_list = Faculty.query.all()
    return render_template('admin/manage_faculty.html', faculty_list=faculty_list)

@admin_bp.route('/add_faculty', methods=['POST'])
@login_required
@admin_required
def add_faculty():
    name = request.form.get('name')
    email = request.form.get('email')
    department = request.form.get('department')
    designation = request.form.get('designation')
    password = request.form.get('password')

    if User.query.filter_by(email=email).first():
        flash('Email already registered!', 'danger')
        return redirect(url_for('admin.manage_faculty'))

    user = User(email=email, role='faculty')
    user.set_password(password)
    db.session.add(user)
    db.session.commit()

    faculty = Faculty(user_id=user.id, name=name, department=department, designation=designation)
    db.session.add(faculty)
    db.session.commit()

    flash('Faculty member added successfully!', 'success')
    flash('Faculty member added successfully!', 'success')
    return redirect(url_for('admin.manage_faculty'))

@admin_bp.route('/edit_faculty/<int:faculty_id>', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_faculty(faculty_id):
    faculty = Faculty.query.get_or_404(faculty_id)
    
    if request.method == 'POST':
        faculty.name = request.form.get('name')
        faculty.department = request.form.get('department')
        faculty.designation = request.form.get('designation')
        
        db.session.commit()
        flash('Faculty details updated successfully!', 'success')
        return redirect(url_for('admin.manage_faculty'))
        
    return render_template('admin/edit_faculty.html', faculty=faculty)

@admin_bp.route('/manage_industries')
@login_required
@admin_required
def manage_industries():
    industries = Industry.query.all()
    return render_template('admin/manage_industries.html', industries=industries)

@admin_bp.route('/edit_industry/<int:industry_id>', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_industry(industry_id):
    industry = Industry.query.get_or_404(industry_id)
    
    if request.method == 'POST':
        industry.name = request.form.get('name')
        industry.location = request.form.get('location')
        industry.contact_person = request.form.get('contact_person')
        industry.email = request.form.get('email')
        industry.phone = request.form.get('phone')
        
        db.session.commit()
        flash('Industry updated successfully!', 'success')
        return redirect(url_for('admin.manage_industries'))
        
    return render_template('admin/edit_industry.html', industry=industry)

@admin_bp.route('/manage_visits')
@login_required
@admin_required
def manage_visits():
    visits = Visit.query.order_by(Visit.visit_date.desc()).all()
    return render_template('admin/manage_visits.html', visits=visits)

@admin_bp.route('/edit_visit/<int:visit_id>', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_visit(visit_id):
    visit = Visit.query.get_or_404(visit_id)
    industries = Industry.query.all()
    faculties = Faculty.query.all()
    
    if request.method == 'POST':
        visit.industry_id = request.form.get('industry')
        visit.title = request.form.get('title')
        visit.description = request.form.get('description')
        visit_date_str = request.form.get('visit_date')
        visit.visit_date = datetime.strptime(visit_date_str, '%Y-%m-%d').date()
        
        new_fee = float(request.form.get('fee'))
        visit.fee = new_fee
        
        new_total_seats = int(request.form.get('total_seats'))
        # Adjust available seats if total seats changed
        seat_diff = new_total_seats - visit.total_seats
        visit.total_seats = new_total_seats
        visit.available_seats += seat_diff 
        
        visit.faculty_id = request.form.get('faculty')
        
        db.session.commit()
        flash('Visit details updated successfully!', 'success')
        return redirect(url_for('admin.manage_visits'))
        
    return render_template('admin/edit_visit.html', visit=visit, industries=industries, faculties=faculties)

@admin_bp.route('/download_report/<type>')
@login_required
@admin_required
def download_report(type):
    if type == 'students_csv':
        students = Student.query.all()
        output = io.StringIO()
        writer = csv.writer(output)
        writer.writerow(['Name', 'Register No', 'Department', 'Year'])
        for s in students:
            writer.writerow([s.name, s.register_number, s.department, s.year])
        
        response = make_response(output.getvalue())
        response.headers["Content-Disposition"] = "attachment; filename=students_report.csv"
        response.headers["Content-type"] = "text/csv"
        return response

    elif type == 'students_pdf':
        students = Student.query.all()
        buffer = io.BytesIO()
        p = canvas.Canvas(buffer)
        p.drawString(100, 800, "Student Participation Report")
        y = 750
        for s in students:
            p.drawString(100, y, f"{s.name} - {s.register_number} ({s.department})")
            y -= 20
        p.showPage()
        p.save()
        buffer.seek(0)
        
        response = make_response(buffer.getvalue())
        response.headers["Content-Disposition"] = "attachment; filename=students_report.pdf"
        response.headers["Content-type"] = "application/pdf"
        return response

    elif type == 'payments':
        payments = Payment.query.all()
        output = io.StringIO()
        writer = csv.writer(output)
        writer.writerow(['ID', 'Booking ID', 'Amount', 'Date', 'Transaction ID'])
        for p in payments:
            writer.writerow([p.id, p.booking_id, p.amount, p.payment_date, p.transaction_id])
        
        response = make_response(output.getvalue())
        response.headers["Content-Disposition"] = "attachment; filename=payment_report.csv"
        response.headers["Content-type"] = "text/csv"
        return response
    
    elif type == 'feedback':
        feedbacks = Feedback.query.all()
        output = io.StringIO()
        writer = csv.writer(output)
        writer.writerow(['Student', 'Visit', 'Rating', 'Comments'])
        for f in feedbacks:
            writer.writerow([f.student_id, f.visit_id, f.rating, f.comments])
            
        response = make_response(output.getvalue())
        response.headers["Content-Disposition"] = "attachment; filename=feedback_report.csv"
        response.headers["Content-type"] = "text/csv"
        return response
    
    flash('Invalid report type selected.', 'danger')
    return redirect(url_for('admin.reports'))
