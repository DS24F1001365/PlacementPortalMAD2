from flask import Flask
from flask_cors import CORS

from models import db, User, Student, Company, PlacementDrive, Application, create_admin

from flask import request                                   #for receiving data from frontend
from flask import jsonify                                   #for converting python dicts to json when sending responses to frontend

from flask_jwt_extended import JWTManager                   #for enabling flask to work with jwt tokens and functions
from flask_jwt_extended import create_access_token, get_jwt_identity          

from datetime import timedelta, datetime

from werkzeug.security import generate_password_hash, check_password_hash           #for verifying passwords since they're stored as hash

from auth import admin_required
from auth import student_required
from auth import company_required

app = Flask(__name__)

CORS(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ppa.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.config['JWT_SECRET_KEY'] = 'PPA_MAD2_SECRET_KEY'
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(days=1)

jwt = JWTManager(app)

db.init_app(app)

with app.app_context():
    db.create_all()
    create_admin()


# ----------------------
# API ENDPOINTS
# ----------------------

@app.route('/api/student/register', methods=['POST'])
def student_register():

    data = request.get_json()

    name = data.get('name')
    email = data.get('email')
    password = data.get('password')
    phone = data.get('phone')
    branch = data.get('branch')
    year = data.get('year')
    cgpa = data.get('cgpa')

    if not all([name, email, password, phone, branch, year, cgpa]):
        return jsonify({
            "success": False,
            "message": "Please fill all required fields."
        }), 400
    if len(password) < 6:
        return jsonify({
            "success": False,
            "message": "Password must be at least 6 characters long."
        }), 400
    
    try:
        year = int(year)
        cgpa = float(cgpa)
    except (TypeError, ValueError):
        return jsonify({
            "success": False,
            "message": "Year and CGPA must be valid numbers."
        }), 400
    if year not in [1, 2, 3, 4]:
        return jsonify({
            "success": False,
            "message": "Year must be between 1 and 4."
        }), 400
    if not (0 <= cgpa <= 10):
        return jsonify({
            "success": False,
            "message": "CGPA must be between 0 and 10."
        }), 400
    
    existing_user = User.query.filter_by(email=email).first()
    if existing_user:
        return jsonify({
            "success": False,
            "message": "Email already registered."
        }), 400
    
    new_user = User(
        name=name,
        email=email,
        password_hash=generate_password_hash(password),
        role='student'
    )
    db.session.add(new_user)
    db.session.commit()

    new_student = Student(
        user_id=new_user.id,
        phone=phone,
        branch=branch,
        year=year,
        cgpa=float(cgpa)
    )
    db.session.add(new_student)
    db.session.commit()
    
    return jsonify({
        "success": True,
        "message": "Student registered successfully."
    }), 201


@app.route('/api/company/register', methods=['POST'])
def company_register():

    data = request.get_json()

    name = data.get('name')
    email = data.get('email')
    password = data.get('password')
    hr_name = data.get('hr_name')
    hr_email = data.get('hr_email')
    hr_contact = data.get('hr_contact')
    website = data.get('website')
    description = data.get('description')

    if not all([name, email, password, hr_name, hr_email, hr_contact]):
        return jsonify({
            "success": False,
            "message": "Please fill all required fields."
        }), 400
    if len(password) < 6:
        return jsonify({
            "success": False,
            "message": "Password must be at least 6 characters long."
        }), 400

    existing_user = User.query.filter_by(email=email).first()
    if existing_user:
        return jsonify({
            "success": False,
            "message": "Email already exists."
        }), 400

    new_user = User(
        name=name,
        email=email,
        password_hash=generate_password_hash(password),
        role="company"
    )
    db.session.add(new_user)
    db.session.commit()

    new_company = Company(
        user_id=new_user.id,
        hr_name=hr_name,
        hr_email=hr_email,
        hr_contact=hr_contact,
        website=website,
        description=description
    )
    db.session.add(new_company)
    db.session.commit()

    return jsonify({
        "success": True,
        "message": "Company registered successfully. Waiting for admin approval."
    }), 201


@app.route('/api/login', methods=['POST'])
def login():

    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    user = User.query.filter_by(email=email).first()

    if not user:
        return jsonify({
            "success": False,
            "message": "Invalid email or password."
        }), 401
    if not check_password_hash(user.password_hash, password):
        return jsonify({
            "success": False,
            "message": "Invalid email or password."
        }), 401
    if user.blacklist_status:
        return jsonify({
            "success": False,
            "message": "Your account has been blacklisted."
        }), 403
    
    access_token = create_access_token(
                identity=str(user.id),
                additional_claims={
                        "role": user.role
                        },
                expires_delta=timedelta(days=1)
                )
    
    return jsonify({
        "success": True,
        "message": "Login successful.",
        "token": access_token,
        "role": user.role,
        "name": user.name,
        "user_id": user.id
    }), 200


# ----------------------
# DASHBOARD APIs
# ----------------------

@app.route('/api/admin/dashboard')
@admin_required
def admin_dashboard():

    user_id = get_jwt_identity()

    user = User.query.get(user_id)
    
    total_students = Student.query.count()
    total_companies = Company.query.count()
    total_drives = PlacementDrive.query.count()
    total_applications = Application.query.count()
    placed_students = Student.query.filter_by(is_placed=True).count()
    pending_companies = Company.query.filter_by(approval_status="Pending").count()
    pending_drives = PlacementDrive.query.filter_by(status="Pending").count()

    return jsonify({
        "success": True,
        "message": "Welcome " + user.name,
        "stats": {
            "total_students": total_students,
            "total_companies": total_companies,
            "total_drives": total_drives,
            "total_applications": total_applications,
            "placed_students": placed_students,
            "pending_companies": pending_companies,
            "pending_drives": pending_drives
        }
    })


@app.route('/api/student/dashboard')
@student_required
def student_dashboard():

    user_id = get_jwt_identity()

    user = User.query.get(user_id)

    return jsonify({
        "success": True,
        "message": "Welcome " + user.name
    })


@app.route('/api/company/dashboard')
@company_required
def company_dashboard():

    user_id = get_jwt_identity()

    user = User.query.get(user_id)

    return jsonify({
        "success": True,
        "message": "Welcome " + user.name
    })


# ----------------------
# ADMIN COMPANY APIs
# ----------------------

@app.route('/api/admin/companies')
@admin_required
def get_companies():

    companies = Company.query.all()
    company_list = []
    for company in companies:
        company_list.append({
            "id": company.id,
            "name": company.user.name,
            "email": company.user.email,
            "hr_name": company.hr_name,
            "hr_email": company.hr_email,
            "approval_status": company.approval_status,
            "blacklist_status": company.user.blacklist_status
        })

    return jsonify({
        "success": True,
        "companies": company_list
    })


@app.route('/api/admin/company/approve/<int:company_id>', methods=['PUT'])
@admin_required
def approve_company(company_id):
    company = Company.query.get(company_id)
    if not company:
        return jsonify({
            "success": False,
            "message": "Company not found"
        }), 404

    company.approval_status = "Approved"
    db.session.commit()
    return jsonify({
        "success": True,
        "message": "Company approved successfully"
    })

@app.route('/api/admin/company/reject/<int:company_id>', methods=['PUT'])
@admin_required
def reject_company(company_id):
    company = Company.query.get(company_id)
    if not company:
        return jsonify({
            "success": False,
            "message": "Company not found"
        }), 404

    company.approval_status = "Rejected"
    db.session.commit()
    return jsonify({
        "success": True,
        "message": "Company rejected successfully"
    })

@app.route('/api/admin/company/blacklist/<int:company_id>', methods=['PUT'])
@admin_required
def blacklist_company(company_id):
    company = Company.query.get(company_id)
    if not company:
        return jsonify({
            "success": False,
            "message": "Company not found"
        }), 404

    company.user.blacklist_status = True
    for drive in company.drives:
        drive.status = "Cancelled"
    db.session.commit()
    return jsonify({
        "success": True,
        "message": "Company blacklisted successfully"
    })

@app.route('/api/admin/company/<int:company_id>')
@admin_required
def view_company(company_id):
    company = Company.query.get(company_id)
    if not company:
        return jsonify({
            "success": False,
            "message": "Company not found"
        }), 404

    return jsonify({
        "success": True,
        "company": {
            "name": company.user.name,
            "email": company.user.email,
            "hr_name": company.hr_name,
            "hr_email": company.hr_email,
            "hr_contact": company.hr_contact,
            "website": company.website,
            "description": company.description,
            "approval_status": company.approval_status,
            "blacklist_status": company.user.blacklist_status
        }
    })

# ----------------------
# ADMIN STUDENT APIs
# ----------------------

@app.route('/api/admin/students')
@admin_required
def get_students():
    students = Student.query.all()
    student_list = []
    for student in students:
        student_list.append({
            "id": student.id,
            "name": student.user.name,
            "email": student.user.email,
            "phone": student.phone,
            "branch": student.branch,
            "is_active": student.is_active,
            "is_placed": student.is_placed,
            "blacklist_status": student.user.blacklist_status
        })

    return jsonify({
        "success": True,
        "students": student_list
    })

@app.route('/api/admin/student/<int:student_id>')
@admin_required
def view_student(student_id):
    student = Student.query.get(student_id)
    if not student:
        return jsonify({
            "success": False,
            "message": "Student not found"
        }), 404

    return jsonify({
        "success": True,
        "student": {
            "name": student.user.name,
            "email": student.user.email,
            "phone": student.phone,
            "branch": student.branch,
            "year": student.year,
            "cgpa": student.cgpa,
            "linkedin": student.linkedin,
            "github": student.github,
            "skills": student.skills,
            "resume_path": student.resume_path,
            "is_active": student.is_active,
            "is_placed": student.is_placed,
            "blacklist_status": student.user.blacklist_status
        }
    })

@app.route('/api/admin/student/toggle-active/<int:student_id>', methods=['PUT'])
@admin_required
def toggle_student_active(student_id):
    student = Student.query.get(student_id)
    if not student:
        return jsonify({
            "success": False,
            "message": "Student not found"
        }), 404

    student.is_active = not student.is_active
    db.session.commit()
    return jsonify({
        "success": True,
        "message": "Student status updated"
    })

@app.route('/api/admin/student/toggle-blacklist/<int:student_id>', methods=['PUT'])
@admin_required
def toggle_student_blacklist(student_id):
    student = Student.query.get(student_id)
    if not student:
        return jsonify({
            "success": False,
            "message": "Student not found"
        }), 404

    student.user.blacklist_status = not student.user.blacklist_status
    db.session.commit()
    return jsonify({
        "success": True,
        "message": "Blacklist status updated"
    })

# ----------------------
# ADMIN DRIVE APIs
# ----------------------

@app.route('/api/admin/drives')
@admin_required
def get_drives():
    drives = PlacementDrive.query.all()
    drive_list = []

    for drive in drives:
        drive_list.append({
            "id": drive.id,
            "title": drive.job_title,
            "specialization": drive.specialization,
            "company": drive.company.user.name,
            "deadline": drive.deadline.strftime("%Y-%m-%d"),
            "status": drive.status
        })

    return jsonify({
        "success": True,
        "drives": drive_list
    })

@app.route('/api/admin/drive/approve/<int:drive_id>', methods=['PUT'])
@admin_required
def approve_drive(drive_id):
    drive = PlacementDrive.query.get(drive_id)
    if not drive:
        return jsonify({
            "success": False,
            "message": "Drive not found"
        }), 404

    drive.status = "Approved"
    db.session.commit()
    return jsonify({
        "success": True,
        "message": "Drive approved successfully"
    })

@app.route('/api/admin/drive/reject/<int:drive_id>', methods=['PUT'])
@admin_required
def reject_drive(drive_id):
    drive = PlacementDrive.query.get(drive_id)
    if not drive:
        return jsonify({
            "success": False,
            "message": "Drive not found"
        }), 404

    drive.status = "Rejected"
    db.session.commit()
    return jsonify({
       "success": True,
        "message": "Drive rejected successfully"
    })

@app.route('/api/admin/drive/<int:drive_id>')
@admin_required
def view_drive(drive_id):
    drive = PlacementDrive.query.get(drive_id)
    if not drive:
        return jsonify({
            "success": False,
            "message": "Drive not found"
        }), 404

    return jsonify({
        "success": True,
        "drive": {
            "title": drive.job_title,
            "specialization": drive.specialization,
            "description": drive.description,
            "company": drive.company.user.name,
            "eligible_branches": drive.eligible_branches,
            "minimum_cgpa": drive.minimum_cgpa,
            "eligible_year": drive.eligible_year,
            "deadline": drive.deadline.strftime("%Y-%m-%d"),
            "status": drive.status
        }

    })


# ----------------------
# ADMIN APPLICATION, PLACEMENT AND STATS APIs
# ----------------------

@app.route('/api/admin/applications')
@admin_required
def get_applications():
    applications = Application.query.all()
    application_list = []

    for application in applications:
        student = application.student
        drive = application.drive

        if student.user.blacklist_status:
            student_status = "Blacklisted"
        elif not student.is_active:
            student_status = "Inactive"
        elif student.is_placed:
            student_status = "Placed"
        else:
            student_status = "Active"

        application_list.append({
            "id": application.id,
            "student_name": student.user.name,
            "drive_id": drive.id,
            "title": drive.job_title,
            "company_name": drive.company.user.name,
            "application_status": application.application_status,
            "offer_status": application.offer_status,
            "student_status": student_status
        })

    return jsonify({
        "success": True,
        "applications": application_list
    })

@app.route('/api/admin/placement-history')
@admin_required
def placement_history():
    placements = Application.query.filter_by(
        application_status="Selected",
        offer_status="Accepted"
    ).all()

    placement_list = []
    for application in placements:
        placement_list.append({
            "id": application.id,
            "student_name": application.student.user.name,
            "company_name": application.drive.company.user.name,
            "drive_title": application.drive.job_title,
            "branch": application.student.branch,
            "cgpa": application.student.cgpa,
            "applied_on": application.applied_on.strftime("%Y-%m-%d")
        })

    return jsonify({
        "success": True,
        "placements": placement_list
    })

@app.route('/api/admin/statistics')
@admin_required
def admin_statistics():

    companies = Company.query.all()
    company_names = []
    applied_counts = []
    selected_counts = []
    accepted_counts = []

    for company in companies:
        company_names.append(company.user.name)

        applied = Application.query.join(PlacementDrive).filter(
            PlacementDrive.company_id == company.id
        ).count()

        selected = Application.query.join(PlacementDrive).filter(
            PlacementDrive.company_id == company.id,
            Application.application_status == "Selected"
        ).count()

        accepted = Application.query.join(PlacementDrive).filter(
            PlacementDrive.company_id == company.id,
            Application.application_status == "Selected",
            Application.offer_status == "Accepted"
        ).count()

        applied_counts.append(applied)
        selected_counts.append(selected)
        accepted_counts.append(accepted)

    return jsonify({
        "success": True,
        "statistics": {
            "companies": company_names,
            "applied": applied_counts,
            "selected": selected_counts,
            "accepted": accepted_counts
        }
    })

# ----------------------
# MAIN
# ----------------------
if __name__ == "__main__":

    app.run(debug=True)