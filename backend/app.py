from flask import Flask
from flask_cors import CORS

from models import db, User, Student, Company, PlacementDrive, Application, create_admin

from flask import request                                   #for receiving data from frontend
from flask import jsonify                                   #for converting python dicts to json when sending responses to frontend

from flask_jwt_extended import JWTManager                   #for enabling flask to work with jwt tokens and functions
from flask_jwt_extended import create_access_token, get_jwt_identity          

from datetime import timedelta, datetime, date

from werkzeug.security import generate_password_hash, check_password_hash           #for verifying passwords since they're stored as hash

import os
from werkzeug.utils import secure_filename                  #for resume file naming
from flask import send_from_directory                       #for viewing resumes and CSVs

from auth import admin_required
from auth import student_required
from auth import company_required

from flask_caching import Cache                             #for redis caching
from cache_helpers import company_dashboard_cache_key
from cache_helpers import  student_dashboard_cache_key

from celery.result import AsyncResult                       #for csv export backend job
from celery_app import export_student_applications

from config import Config


app = Flask(__name__)
cache = Cache()

CORS(app)

app.config.from_object(Config)

#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ppa.db'
#app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

#app.config['JWT_SECRET_KEY'] = 'PPA_MAD2_SECRET_KEY'
#app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(days=1)

#app.config["CACHE_TYPE"] = "RedisCache"
#app.config["CACHE_REDIS_HOST"] = "localhost"
#app.config["CACHE_REDIS_PORT"] = 6379
#app.config["CACHE_DEFAULT_TIMEOUT"] = 60

UPLOAD_FOLDER = os.path.join(app.root_path,"uploads","resumes")
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

jwt = JWTManager(app)

db.init_app(app)
cache.init_app(app)
print(cache.cache)

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
@cache.cached(timeout=60)
@admin_required
def admin_dashboard():
    print("ADMIN DASHBOARD EXECUTED")

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


@app.route('/api/student/dashboard', methods=['GET'])
@cache.cached(timeout=60,make_cache_key=student_dashboard_cache_key)
@student_required
def student_dashboard():
    print("STUDENT")
    user_id = get_jwt_identity()
    student = Student.query.filter_by(user_id=user_id).first()
    total_applications = Application.query.filter_by(student_id=student.id).count()
    selected_applications = Application.query.filter_by(
        student_id=student.id,
        application_status="Selected"
    ).count()
    pending_offers = Application.query.filter_by(
        student_id=student.id,
        offer_status="Pending"
    ).count()

    return jsonify({
        "success": True,
        "message": "Welcome " + student.user.name,
        "is_placed": student.is_placed,
        "stats": {
            "total_applications": total_applications,
            "selected_applications": selected_applications,
            "pending_offers": pending_offers

        }

    })


@app.route('/api/company/dashboard')
@cache.cached(timeout=60, make_cache_key=company_dashboard_cache_key)
@company_required
def company_dashboard():
    print("COMPANY")
    user_id = get_jwt_identity()
    company = Company.query.filter_by(user_id=user_id).first()

    total_drives = PlacementDrive.query.filter_by(company_id=company.id).count()
    approved_drives = PlacementDrive.query.filter_by(
        company_id=company.id,
        status="Approved"
        ).count()
    total_applicants = Application.query.join(PlacementDrive).filter(PlacementDrive.company_id == company.id).count()
    pending_applications = (
        Application.query
        .join(Student, Application.student_id == Student.id)
        .join(User, Student.user_id == User.id)
        .join(PlacementDrive, Application.drive_id == PlacementDrive.id)
        .filter(
            PlacementDrive.company_id == company.id,
            Application.application_status == "Applied",
            Student.is_active == True,
            Student.is_placed == False,
            User.blacklist_status == False
        )
        .count()
    )
    selected_students = Application.query.join(PlacementDrive).filter(
        PlacementDrive.company_id == company.id,
        Application.application_status == "Selected"
        ).count()
    company_drives = PlacementDrive.query.filter_by(company_id=company.id).all()

    pending_drive_list = []

    for drive in company_drives:
        count = (
            Application.query
            .join(Student, Application.student_id == Student.id)
            .join(User, Student.user_id == User.id)
            .filter(
                Application.drive_id == drive.id,
                Application.application_status == "Applied",
                Student.is_active == True,
                Student.is_placed == False,
                User.blacklist_status == False
                ).count()
            )
        if count > 0:
            pending_drive_list.append({
                "drive_id": drive.id,
                "title": drive.job_title,
                "pending_count": count
            })

    return jsonify({
        "success": True,
        "message": "Welcome " + company.user.name,
        "stats": {
            "total_drives": total_drives,
            "approved_drives": approved_drives,
            "total_applicants": total_applicants,
            "pending_applications": pending_applications,
            "selected_students": selected_students
            },
        "pending_drives": pending_drive_list
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
@cache.cached(timeout=60)
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
# COMPANY PROFILE APIs
# ----------------------

@app.route('/api/company/profile', methods=['GET'])
@company_required
def get_company_profile():

    user_id = get_jwt_identity()
    company = Company.query.filter_by(user_id=user_id).first()

    return jsonify({
        "success": True,
        "profile": {
            "company_name": company.user.name,
            "email": company.user.email,
            "hr_name": company.hr_name,
            "hr_email": company.hr_email,
            "hr_contact": company.hr_contact,
            "website": company.website,
            "description": company.description
        }
    })

@app.route('/api/company/profile', methods=['PUT'])
@company_required
def update_company_profile():

    user_id = get_jwt_identity()
    company = Company.query.filter_by(user_id=user_id).first()

    data = request.get_json()

    company.hr_name = data.get("hr_name", company.hr_name)
    company.hr_email = data.get("hr_email", company.hr_email)
    company.hr_contact = data.get("hr_contact", company.hr_contact)
    company.website = data.get("website", company.website)
    company.description = data.get("description", company.description)
    db.session.commit()
    return jsonify({
        "success": True,
        "message": "Profile updated successfully"
    })

# ----------------------
# COMPANY DRIVE APIs
# ----------------------

@app.route('/api/company/drives', methods=['GET'])
@company_required
def get_company_drives():

    user_id = get_jwt_identity()
    company = Company.query.filter_by(user_id=user_id).first()
    drives = PlacementDrive.query.filter_by(company_id=company.id).all()

    drive_list = []
    for drive in drives:
        drive_list.append({
            "id": drive.id,
            "job_title": drive.job_title,
            "specialization": drive.specialization,
            "deadline": drive.deadline.strftime("%Y-%m-%d"),
            "status": drive.status
        })

    return jsonify({
        "success": True,
        "drives": drive_list
    })

@app.route('/api/company/drives', methods=['POST'])
@company_required
def create_company_drive():

    user_id = get_jwt_identity()
    company = Company.query.filter_by(user_id=user_id).first()

    data = request.get_json()
    job_title = data.get("job_title")
    eligible_branches = data.get("eligible_branches")
    minimum_cgpa = data.get("minimum_cgpa")
    eligible_year = data.get("eligible_year")
    deadline = datetime.strptime(data.get("deadline"),"%Y-%m-%d").date()
    if (
    not job_title
    or not eligible_branches
    or minimum_cgpa is None
    or eligible_year is None
    or not deadline
    ):
        return jsonify({
        "success": False,
        "message": "Please fill all mandatory fields."
    }), 400

    if deadline < date.today():
        return jsonify({
            "success": False,
            "message": "Deadline cannot be in the past"
        }), 400
    
    if minimum_cgpa < 0 or minimum_cgpa > 10:
        return jsonify({
            "success": False,
            "message": "Minimum CGPA must be between 0 and 10."
        }), 400

    drive = PlacementDrive(
        company_id = company.id,
        job_title = data.get("job_title"),
        specialization = data.get("specialization"),
        description = data.get("description"),
        eligible_branches = ",".join(data.get("eligible_branches", [])),
        eligible_year = data.get("eligible_year"),
        minimum_cgpa = data.get("minimum_cgpa"),
        deadline = deadline
        )

    db.session.add(drive)
    db.session.commit()
    return jsonify({
        "success": True,
        "message": "Placement drive created successfully"
    })

@app.route('/api/company/drive/<int:drive_id>', methods=['GET'])
@company_required
def get_company_drive(drive_id):

    user_id = get_jwt_identity()
    company = Company.query.filter_by(user_id=user_id).first()
    drive = PlacementDrive.query.filter_by(id=drive_id, company_id=company.id).first()
    if not drive:
        return jsonify({
            "success": False,
            "message": "Drive not found"
        }),404
    
    if drive.status != "Pending":
        return jsonify({
            "success": False,
            "message": "Only pending drives can be edited"
        }), 400    

    return jsonify({
        "success": True,
        "drive":{
            "job_title":drive.job_title,
            "specialization":drive.specialization,
            "description":drive.description,
            "eligible_branches":drive.eligible_branches,
            "eligible_year":drive.eligible_year,
            "minimum_cgpa":drive.minimum_cgpa,
            "deadline":drive.deadline.strftime("%Y-%m-%d")
        }
    })

@app.route('/api/company/drive/<int:drive_id>', methods=['PUT'])
@company_required
def edit_company_drive(drive_id):

    user_id = get_jwt_identity()
    company = Company.query.filter_by(user_id=user_id).first()
    drive = PlacementDrive.query.filter_by(id=drive_id, company_id=company.id).first()
    if not drive:
        return jsonify({
            "success": False,
            "message": "Drive not found"
        }), 404

    if drive.status != "Pending":
        return jsonify({
            "success": False,
            "message": "Only pending drives can be edited"
        }), 400

    data = request.get_json()
    drive.job_title = data.get("job_title", drive.job_title)
    drive.specialization = data.get("specialization", drive.specialization)
    drive.description = data.get("description", drive.description)
    if data.get("eligible_branches"):
        drive.eligible_branches = ",".join(data.get("eligible_branches"))
    drive.eligible_year = data.get("eligible_year", drive.eligible_year)
    drive.minimum_cgpa = data.get("minimum_cgpa", drive.minimum_cgpa)
    if data.get("deadline"):
        deadline = datetime.strptime(data.get("deadline"),"%Y-%m-%d").date()
        if deadline < date.today():
            return jsonify({
                "success": False,
                "message": "Deadline cannot be in the past"
            }), 400

        drive.deadline = deadline
        db.session.commit()
        return jsonify({
            "success": True,
            "message": "Drive updated successfully"
        })

@app.route('/api/company/drive/<int:drive_id>', methods=['DELETE'])
@company_required
def delete_company_drive(drive_id):

    user_id = get_jwt_identity()
    company = Company.query.filter_by(user_id=user_id).first()
    drive = PlacementDrive.query.filter_by(id=drive_id,company_id=company.id).first()
    if not drive:
        return jsonify({
            "success": False,
            "message": "Drive not found"
        }), 404

    if drive.status not in ["Pending", "Rejected"]:
        return jsonify({
            "success": False,
            "message": "Only pending or rejected drives can be deleted"
        }), 400

    db.session.delete(drive)
    db.session.commit()
    return jsonify({
        "success": True,
        "message": "Drive deleted successfully"
    })

@app.route('/api/company/drive/close/<int:drive_id>', methods=['PUT'])
@company_required
def close_company_drive(drive_id):

    user_id = get_jwt_identity()
    company = Company.query.filter_by(user_id=user_id).first()
    drive = PlacementDrive.query.filter_by(id=drive_id, company_id=company.id).first()
    if not drive:
        return jsonify({
            "success": False,
            "message": "Drive not found"
        }), 404

    if drive.status != "Approved":
        return jsonify({
            "success": False,
            "message": "Only approved drives can be closed"
        }), 400

    drive.status = "Closed"
    db.session.commit()
    return jsonify({
        "success": True,
        "message": "Drive closed successfully"
    })

@app.route('/api/company/drive/<int:drive_id>/applicants', methods=['GET'])
@company_required
def get_drive_applicants(drive_id):

    user_id = get_jwt_identity()
    company = Company.query.filter_by(user_id=user_id).first()
    drive = PlacementDrive.query.filter_by(id=drive_id,company_id=company.id).first()
    if not drive:
        return jsonify({
            "success": False,
            "message": "Drive not found"
        }), 404

    applications = Application.query.filter_by(drive_id=drive.id).all()
    applicant_list = []
    for application in applications:
        student = Student.query.get(application.student_id)
        user = student.user
        if user.blacklist_status:
            eligibility = "Blacklisted"
        elif not student.is_active:
            eligibility = "Inactive"
        elif student.is_placed:
            eligibility = "Placed"
        else:
            eligibility = "Eligible"

        applicant_list.append({
            "application_id": application.id,
            "student_id": student.id,
            "student_name": user.name,
            "application_status": application.application_status,
            "offer_status": application.offer_status,
            "eligibility": eligibility
        })

    return jsonify({
        "success": True,
        "drive_title": drive.job_title,
        "applicants": applicant_list
    })

@app.route('/api/company/update-application-status/<int:application_id>', methods=['PUT'])
@company_required
def update_application_status(application_id):

    user_id = get_jwt_identity()
    company = Company.query.filter_by(user_id=user_id).first()
    application = Application.query.get(application_id)
    if not application:
        return jsonify({
            "success": False,
            "message": "Application not found"
        }), 404
    
    student = Student.query.get(application.student_id)
    user = student.user
    if user.blacklist_status:
        return jsonify({
            "success": False,
            "message": "Cannot perform actions. Student is blacklisted"
        }), 400
    if not student.is_active:
        return jsonify({
            "success": False,
            "message": "Cannot perform actions. Student is inactive"
        }), 400
    if student.is_placed:
        return jsonify({
            "success": False,
            "message": "Cannot perform actions. Student is already placed"
        }), 400

    drive = PlacementDrive.query.get(application.drive_id)
    if drive.company_id != company.id:
        return jsonify({
            "success": False,
            "message": "Unauthorized"
        }), 403

    data = request.get_json()
    new_status = data.get("application_status")
    valid_statuses = ["Shortlisted","Selected","Rejected"]
    if new_status not in valid_statuses:
        return jsonify({
            "success": False,
            "message": "Invalid application status"
        }), 400
    
    current_status = application.application_status
    if current_status == "Applied":
        allowed = ["Shortlisted","Selected","Rejected"]
    elif current_status == "Shortlisted":
        allowed = ["Selected","Rejected"]
    else:
        allowed = []

    if new_status not in allowed:
        return jsonify({
            "success": False,
            "message": "Invalid status transition"
        }), 400
    
    application.application_status = new_status
    if new_status == "Selected":
        application.offer_status = "Pending"
    #else:
    #    application.offer_status = "NA"

    db.session.commit()
    return jsonify({
        "success": True,
        "message": "Application updated successfully"
    })

@app.route('/api/company/application/<int:application_id>/student', methods=['GET'])
@company_required
def get_applicant_profile(application_id):

    user_id = get_jwt_identity()
    company = Company.query.filter_by(user_id=user_id).first()
    application = Application.query.get(application_id)
    if not application:
        return jsonify({
            "success": False,
            "message": "Application not found"
        }), 404

    drive = PlacementDrive.query.get(application.drive_id)
    if drive.company_id != company.id:
        return jsonify({
            "success": False,
            "message": "Unauthorized"
        }), 403

    student = Student.query.get(application.student_id)
    return jsonify({
        "success": True,
        "student": {
            "name": student.user.name,
            "email": student.user.email,
            "phone": student.phone,
            "branch": student.branch,
            "year": student.year,
            "cgpa": student.cgpa,
            "skills": student.skills,
            "linkedin": student.linkedin,
            "github": student.github,
            "resume_path": student.resume_path
        }
    })


# ----------------------
# STUDENT PROFILE APIs
# ----------------------

@app.route('/api/student/profile', methods=['GET'])
@student_required
def get_student_profile():

    user_id = get_jwt_identity()
    student = Student.query.filter_by(user_id=user_id).first()

    return jsonify({
        "success": True,
        "profile": {
            "name": student.user.name,
            "email": student.user.email,
            "phone": student.phone,
            "branch": student.branch,
            "year": student.year,
            "cgpa": student.cgpa,
            "skills": student.skills,
            "linkedin": student.linkedin,
            "github": student.github,
            "resume_path": student.resume_path,
            "is_active": student.is_active,
            "is_placed": student.is_placed
        }
    })

@app.route('/api/student/profile', methods=['PUT'])
@student_required
def update_student_profile():

    user_id = get_jwt_identity()
    student = Student.query.filter_by(user_id=user_id).first()
    if not student.is_active or student.is_placed:
        return jsonify({
        "success": False,
        "message": "Inactive or Placed students cannot update their profile."
        }), 403
    student.phone = request.form.get("phone",student.phone)
    student.skills = request.form.get("skills",student.skills)
    student.linkedin = request.form.get("linkedin",student.linkedin)
    student.github = request.form.get("github",student.github)
    resume = request.files.get("resume")
    if resume:
        if student.resume_path:
            old_file = os.path.join(app.config["UPLOAD_FOLDER"],student.resume_path)
            if os.path.exists(old_file):
                os.remove(old_file)
        extension = os.path.splitext(secure_filename(resume.filename))[1]
        filename = f"student_{student.id}_resume{extension}"
        filepath = os.path.join(
            app.config["UPLOAD_FOLDER"],
            filename
            )
        resume.save(filepath)
        student.resume_path = filename
    print("CONTENT TYPE:", request.content_type)
    print("FORM:", request.form)
    print("FILES:", request.files)

    db.session.commit()
    return jsonify({
        "success": True,
        "message": "Profile updated successfully"
    })

@app.route('/uploads/resumes/<path:filename>')
def uploaded_resume(filename):   
    return send_from_directory(
        app.config["UPLOAD_FOLDER"],
        filename
    )

# ----------------------
# STUDENT AVAILABLE DRIVE APIs
# ----------------------

@app.route('/api/student/drives', methods=['GET'])
@student_required
def get_available_drives():

    user_id = get_jwt_identity()
    student = Student.query.filter_by(
        user_id=user_id
    ).first()
    today = date.today()
    drives = PlacementDrive.query.filter(
        PlacementDrive.status == "Approved",
        PlacementDrive.deadline >= today
    ).all()

    available_drives = []

    for drive in drives:
        company = Company.query.get(drive.company_id)
        if company.approval_status != "Approved":
           continue
        eligible_branches = [branch.strip() for branch in drive.eligible_branches.split(",")]
        if student.branch not in eligible_branches:
            continue
        if student.year < drive.eligible_year:
            continue
        if student.cgpa < drive.minimum_cgpa:
            continue
        application = Application.query.filter_by(
            student_id=student.id,
            drive_id=drive.id
        ).first()

        available_drives.append({
            "id": drive.id,
            "company": company.user.name,
            "job_title": drive.job_title,
            "specialization": drive.specialization,
            "description": drive.description,
            "deadline": drive.deadline.strftime("%Y-%m-%d"),
            "applied": application is not None
        })

    return jsonify({
        "success": True,
        "drives": available_drives,
        "is_placed": student.is_placed,
        "is_active": student.is_active
    })
    
@app.route('/api/student/apply/<int:drive_id>', methods=['POST'])
@student_required
def apply_for_drive(drive_id):

    user_id = get_jwt_identity()
    student = Student.query.filter_by(user_id=user_id).first()
    if not student.is_active:
        return jsonify({
            "success": False,
            "message": "Inactive students cannot apply."
        }), 403
    if student.is_placed:
        return jsonify({
            "success": False,
            "message": "Placed students cannot apply."
        }), 403

    drive = PlacementDrive.query.get(drive_id)
    if not drive:
        return jsonify({
            "success": False,
            "message": "Drive not found."
        }), 404
    if drive.status != "Approved":
        return jsonify({
            "success": False,
            "message": "Drive is not available."
        }), 400

    if drive.deadline < date.today():
        return jsonify({
            "success": False,
            "message": "Application deadline has passed."
        }), 400

    company = Company.query.get(drive.company_id)
    if company.approval_status != "Approved":
        return jsonify({
            "success": False,
            "message": "Company is not approved."
        }), 400

    eligible_branches = [branch.strip() for branch in drive.eligible_branches.split(",")]
    if student.branch not in eligible_branches:
        return jsonify({
            "success": False,
            "message": "You are not eligible for this drive."
        }), 403

    if student.year < drive.eligible_year:
        return jsonify({
            "success": False,
            "message": "You are not eligible for this drive."
        }), 403

    if student.cgpa < drive.minimum_cgpa:
        return jsonify({
            "success": False,
           "message": "You are not eligible for this drive."
        }), 403

    duplicate = Application.query.filter_by(
        student_id=student.id,
        drive_id=drive.id
    ).first()
    if duplicate:
        return jsonify({
            "success": False,
            "message": "You have already applied."
        }), 400

    application = Application(
        student_id=student.id,
        drive_id=drive.id
    )
    db.session.add(application)
    db.session.commit()
    return jsonify({
        "success": True,
        "message": "Application submitted successfully."
    })

# ----------------------
# STUDENT APPLICATIONS AND OFFERS APIs
# ----------------------

@app.route('/api/student/applications', methods=['GET'])
@student_required
def get_student_applications():

    user_id = get_jwt_identity()
    student = Student.query.filter_by(
        user_id=user_id
    ).first()
    applications = Application.query.filter_by(
        student_id=student.id
    ).all()

    application_list = []

    for application in applications:
        drive = PlacementDrive.query.get(
            application.drive_id
        )
        company = Company.query.get(
            drive.company_id
        )

        if drive.status == "Approved":
            drive_status = "Active"
        else:
            drive_status = drive.status

        application_list.append({
            "id": application.id,
            "company": company.user.name,
            "job_title": drive.job_title,
            "specialization": drive.specialization,
            "application_status": application.application_status,
            "drive_status": drive_status
        })

    return jsonify({
        "success": True,
        "applications": application_list
    })

@app.route('/api/student/offers', methods=['GET'])
@student_required
def get_student_offers():

    user_id = get_jwt_identity()
    student = Student.query.filter_by(user_id=user_id).first()
    applications = Application.query.filter_by(
        student_id=student.id,
        application_status="Selected"
    ).all()

    offers = []

    for application in applications:
        drive = PlacementDrive.query.get(application.drive_id)
        company = Company.query.get(drive.company_id)
        if drive.status == "Approved":
            drive_status = "Active"
        else:
            drive_status = drive.status
        can_respond = (
            student.is_active
            and
            not student.is_placed
            and
            application.offer_status == "Pending"
            and
            drive.status in ["Approved", "Closed"]
        )

        offers.append({
            "application_id": application.id,
            "company": company.user.name,
            "job_title": drive.job_title,
            "specialization": drive.specialization,
            "drive_status": drive_status,
            "offer_status": application.offer_status,
            "can_respond": can_respond
        })

    return jsonify({
        "success": True,
        "is_active": student.is_active,
        "is_placed": student.is_placed,
        "offers": offers
    })

@app.route('/api/student/update-offer-status/<int:application_id>', methods=['PUT'])
@student_required
def update_offer_status(application_id):

    user_id = get_jwt_identity()
    student = Student.query.filter_by(user_id=user_id).first()
    if not student.is_active:
        return jsonify({
            "success": False,
            "message": "Inactive students cannot respond to offers."
        }), 403
    if student.is_placed:
        return jsonify({
            "success": False,
            "message": "You have already accepted an offer."
        }), 403

    application = Application.query.get(application_id)
    if not application:
        return jsonify({
            "success": False,
           "message": "Application not found."
        }), 404
    if application.student_id != student.id:
        return jsonify({
            "success": False,
            "message": "Unauthorized."
        }), 403
    if application.application_status != "Selected":
        return jsonify({
            "success": False,
            "message": "Offer not available."
        }), 400
    if application.offer_status != "Pending":
        return jsonify({
            "success": False,
            "message": "Offer already responded."

        }), 400

    drive = PlacementDrive.query.get(application.drive_id)
    if drive.status == "Cancelled":
        return jsonify({
            "success": False,
            "message": "This offer has been cancelled."
        }), 400

    data = request.get_json()
    offer_status = data.get("offer_status")
    if offer_status not in ["Accepted", "Rejected"]:
        return jsonify({
            "success": False,
            "message": "Invalid offer status."
        }), 400
    if offer_status == "Rejected":
        application.offer_status = "Rejected"
        db.session.commit()
        return jsonify({
            "success": True,
            "message": "Offer rejected."
        })

    application.offer_status = "Accepted"
    student.is_placed = True
    other_offers = Application.query.filter(
        Application.student_id == student.id,
        Application.id != application.id,
        Application.offer_status == "Pending"
    ).all()
    for other in other_offers:
        other.offer_status = "Rejected"

    db.session.commit()
    return jsonify({
        "success": True,
        "message": "Offer accepted successfully."
    })

# ----------------------
# CELERY BACKEND JOBS
# ----------------------

# ----------------------
# CELERY BACKEND JOBS TESTING APIs
# ----------------------
from celery_app import hello
@app.route("/celery-test")
def celery_test():
    hello.delay()
    return "Task sent to Celery!"

from mail_utils import send_email
@app.route("/mail-test")
def mail_test():

    send_email(
        "student@example.com",
        "MailHog Test",
        "<h2>Hello from Placement Portal</h2>"
    )

    return "Mail Sent!"

from celery_app import send_daily_reminders
@app.route("/daily-reminder-test")
def daily_reminder_test():
    task = send_daily_reminders.delay()
    return jsonify({
        "success": True,
        "task_id": task.id
    })

from celery_app import send_monthly_report
@app.route("/monthly-report-test")
def monthly_report_test():
    task = send_monthly_report.delay()
    return jsonify({
        "success":True,
        "task_id":task.id
    })

# ----------------------
# CSV EXPORT
# ----------------------
@app.route("/api/student/export-applications", methods=["POST"])
@student_required
def export_applications():
    user_id = get_jwt_identity()
    student = Student.query.filter_by(
        user_id=user_id
    ).first()

    task = export_student_applications.delay(student.id)
    return jsonify({
        "success": True,
        "message": "Export started",
        "task_id": task.id
    })

@app.route("/api/student/export-status/<task_id>")
@student_required
def export_status(task_id):
    task = AsyncResult(
        task_id,
        app=export_student_applications.app
    )
    response = {"state": task.state}
    if task.state == "SUCCESS":
        response["filename"] = task.result
    return jsonify(response)

@app.route("/api/student/download-export/<filename>")
@student_required
def download_export(filename):
    return send_from_directory(
        "exports",
        filename,
        as_attachment=True
    )

# ----------------------
# MAIN
# ----------------------
if __name__ == "__main__":

    app.run(debug=True)