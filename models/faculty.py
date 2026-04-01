from .db import db

class Faculty(db.Model):
    __tablename__ = 'faculty'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    name = db.Column(db.String(100), nullable=False)
    department = db.Column(db.String(50), nullable=False)
    designation = db.Column(db.String(50), nullable=False)

    user = db.relationship('User', backref=db.backref('faculty_profile', uselist=False))
    visits = db.relationship('Visit', backref='faculty', lazy=True)
