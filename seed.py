from app import create_app
from models.db import db
from models.user import User
from models.admin import Admin
from models.faculty import Faculty

app = create_app()

def seed_users():
    with app.app_context():
        db.create_all()

        # Create Admin
        if not User.query.filter_by(email='admin@college.edu').first():
            admin_user = User(email='admin@college.edu', role='admin')
            admin_user.set_password('admin123')
            db.session.add(admin_user)
            db.session.commit()
            
            admin_profile = Admin(user_id=admin_user.id, name='System Administrator')
            db.session.add(admin_profile)
            print("Admin user created.")

        # Create Faculty
        if not User.query.filter_by(email='faculty@college.edu').first():
            faculty_user = User(email='faculty@college.edu', role='faculty')
            faculty_user.set_password('faculty123')
            db.session.add(faculty_user)
            db.session.commit()
            
            faculty_profile = Faculty(
                user_id=faculty_user.id, 
                name='Dr. Alan Turing', 
                department='CSE', 
                designation='Professor'
            )
            db.session.add(faculty_profile)
            print("Faculty user created.")

        db.session.commit()
        print("Database seeded successfully!")

if __name__ == '__main__':
    seed_users()
