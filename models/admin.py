from .db import db

class Admin(db.Model):
    __tablename__ = 'admins'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    name = db.Column(db.String(100), nullable=False)
    # Admin can have more fields if needed

    user = db.relationship('User', backref=db.backref('admin_profile', uselist=False))
