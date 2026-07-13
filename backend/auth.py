from functools import wraps

from flask import jsonify

from flask_jwt_extended import verify_jwt_in_request
from flask_jwt_extended import get_jwt, get_jwt_identity

from models import Company, Student


# ----------------------
# ADMIN REQUIRED
# ----------------------
def admin_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):

        verify_jwt_in_request()

        claims = get_jwt()
        if claims["role"] != "admin":
            return jsonify({
                "success": False,
                "message": "Admin access required"
            }), 403
        return func(*args, **kwargs)

    return wrapper


# ----------------------
# STUDENT REQUIRED
# ----------------------
def student_required(func):

    @wraps(func)
    def wrapper(*args, **kwargs):

        verify_jwt_in_request()

        claims = get_jwt()
        if claims["role"] != "student":
            return jsonify({
                "success": False,
                "message": "Student access required"
            }), 403
        
        user_id = get_jwt_identity()
        student = Student.query.filter_by(user_id=user_id).first()
        if student.user.blacklist_status:
            return jsonify({
                "success": False,
                "message": "You have been blacklisted. You cannot access student services."
            }), 403

        return func(*args, **kwargs)

    return wrapper


# ----------------------
# COMPANY REQUIRED
# ----------------------
def company_required(func):

    @wraps(func)
    def wrapper(*args, **kwargs):

        verify_jwt_in_request()

        claims = get_jwt()
        if claims["role"] != "company":
            return jsonify({
                "success": False,
                "message": "Company access required"
            }), 403

        user_id = get_jwt_identity()
        company = Company.query.filter_by(user_id=user_id).first()

        if not company:
            return jsonify({
                "success": False,
                "message": "Company profile not found"
            }), 404

        if company.user.blacklist_status:
            return jsonify({
                "success": False,
                "message": "Your company has been blacklisted. You cannot access company services."
            }), 403

        if company.approval_status == "Pending":
            return jsonify({
                "success": False,
                "message": "Your company registration is waiting for admin approval."
            }), 403

        if company.approval_status == "Rejected":
            return jsonify({
                "success": False,
                "message": "Your company registration has been rejected."
            }), 403

        return func(*args, **kwargs)

    return wrapper