from .db import db

class Industry(db.Model):
    __tablename__ = 'industries'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    location = db.Column(db.String(200), nullable=False)
    contact_person = db.Column(db.String(100))
    email = db.Column(db.String(120))
    phone = db.Column(db.String(20))
    
    visits = db.relationship('Visit', backref='industry', lazy=True)
