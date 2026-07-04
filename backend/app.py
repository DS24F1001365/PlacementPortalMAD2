from flask import Flask
from flask_cors import CORS

from models import db, User, Student, Company, PlacementDrive, Application, create_admin

from flask import request                                   #for receiving data from frontend
from flask import jsonify                                   #for converting python dicts to json when sending responses to frontend

from flask_jwt_extended import JWTManager                   #for enabling flask to work with jwt tokens and functions
from flask_jwt_extended import create_access_token, get_jwt_identity          

from datetime import timedelta                              

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

    return jsonify({
        "success": True,
        "message": "Welcome " + user.name
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
# MAIN
# ----------------------
if __name__ == "__main__":

    app.run(debug=True)