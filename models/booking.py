from .db import db
from datetime import datetime

class Booking(db.Model):
    __tablename__ = 'bookings'

    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('students.id'), nullable=False)
    visit_id = db.Column(db.Integer, db.ForeignKey('visits.id'), nullable=False)
    
    booking_date = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.String(20), default='Pending') # Pending, Approved, Rejected, Confirmed (after payment)
    payment_status = db.Column(db.String(20), default='Unpaid') # Unpaid, Paid
    
    qr_code_path = db.Column(db.String(200)) # Path to generated QR

    payment = db.relationship('Payment', backref='booking', uselist=False)
    attendance = db.relationship('Attendance', backref='booking', uselist=False)
    student_profile = db.relationship('Student', backref='bookings')
