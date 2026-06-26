from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from werkzeug.security import generate_password_hash


db = SQLAlchemy()

# ----------------------
# USER TABLE (Common Login)
# ----------------------
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20), nullable=False)  # admin/student/company
    blacklist_status = db.Column(db.Boolean, default=False)

    student = db.relationship('Student', backref='user', uselist=False)
    company = db.relationship('Company', backref='user', uselist=False)


# ----------------------
# STUDENT TABLE
# ----------------------
class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    phone = db.Column(db.String(15))
    branch = db.Column(db.String(100))
    year = db.Column(db.Integer)
    cgpa = db.Column(db.Float)
    linkedin = db.Column(db.String(200))
    github = db.Column(db.String(200))
    skills = db.Column(db.String(300))
    resume_path = db.Column(db.String(200))
    is_active = db.Column(db.Boolean, default=True)
    is_placed = db.Column(db.Boolean, default=False)
# ----------------------
# STUDENT TABLE EXTENSION
# ----------------------
    applications = db.relationship('Application', backref='student', cascade="all, delete", lazy=True)


# ----------------------
# COMPANY TABLE
# ----------------------
class Company(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    hr_name = db.Column(db.String(100))
    hr_email = db.Column(db.String(100))
    hr_contact = db.Column(db.String(100))
    website = db.Column(db.String(200))
    description = db.Column(db.Text)
    approval_status = db.Column(db.String(20), default="Pending")  # Pending/Approved/Rejected
# ----------------------
# COMPANY TABLE EXTENSION
# ----------------------
    drives = db.relationship('PlacementDrive', backref='company', cascade="all, delete", lazy=True)


# ----------------------
# PLACEMENT DRIVE TABLE
# ----------------------
class PlacementDrive(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    company_id = db.Column(db.Integer, db.ForeignKey('company.id'), nullable=False)

    job_title = db.Column(db.String(150), nullable=False)
    specialization = db.Column(db.String(100))   
    description = db.Column(db.Text)
    eligible_branches = db.Column(db.String(200))
    minimum_cgpa = db.Column(db.Float)
    eligible_year = db.Column(db.Integer)
    deadline = db.Column(db.Date, nullable=False)

    status = db.Column(db.String(20), default="Pending")#Pending/Approved/Rejected/Cancelled

    applications = db.relationship('Application', backref='drive', cascade="all, delete", lazy=True)

    __table_args__ = (
        db.UniqueConstraint(
            'company_id',
            'job_title',
            'specialization',
            'deadline',
            name='unique_company_drive'
        ),
    )


# ----------------------
# APPLICATION TABLE
# ----------------------
class Application(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    student_id = db.Column(db.Integer, db.ForeignKey('student.id'), nullable=False)
    drive_id = db.Column(db.Integer, db.ForeignKey('placement_drive.id'), nullable=False)

    applied_on = db.Column(db.DateTime, default=datetime.utcnow)
    application_status = db.Column(db.String(20), default="Applied")  # Applied/Shortlisted/Selected/Rejected
    offer_status = db.Column(db.String(20), default="Pending")# Pending / Accepted / Declined

    # Prevent duplicate application
    __table_args__ = (
        db.UniqueConstraint('student_id', 'drive_id', name='unique_application'),
    )


# ----------------------
# ADMIN CREATION FUNCTION
# ----------------------
def create_admin():
    admin = User.query.filter_by(email='admin@ppa.com').first()
    if not admin:
        admin = User(name='admin',
                     email='admin@ppa.com',
                     password_hash=generate_password_hash('admin123'),
                     role='admin'
                    )
        db.session.add(admin)
        db.session.commit()