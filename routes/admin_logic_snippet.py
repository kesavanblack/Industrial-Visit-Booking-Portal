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
    return redirect(url_for('admin.manage_faculty'))

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
