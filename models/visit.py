from .db import db
from datetime import datetime

class Visit(db.Model):
    __tablename__ = 'visits'

    id = db.Column(db.Integer, primary_key=True)
    industry_id = db.Column(db.Integer, db.ForeignKey('industries.id'), nullable=False)
    faculty_id = db.Column(db.Integer, db.ForeignKey('faculty.id'), nullable=True) # Coordinator
    
    visit_date = db.Column(db.Date, nullable=False)
    title = db.Column(db.String(200), nullable=False) # e.g., "Visit to InfoTech Solutions"
    description = db.Column(db.Text)
    fee = db.Column(db.Float, default=0.0)
    total_seats = db.Column(db.Integer, nullable=False)
    available_seats = db.Column(db.Integer, nullable=False)
    status = db.Column(db.String(20), default='Upcoming') # Upcoming, Completed, Cancelled
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    bookings = db.relationship('Booking', backref='visit', lazy=True)
    feedbacks = db.relationship('Feedback', backref='visit', lazy=True)
