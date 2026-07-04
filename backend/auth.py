from functools import wraps

from flask import jsonify

from flask_jwt_extended import verify_jwt_in_request
from flask_jwt_extended import get_jwt


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

        return func(*args, **kwargs)

    return wrapper