from flask_jwt_extended import (
    verify_jwt_in_request,
    get_jwt_identity
)

def company_dashboard_cache_key():
    verify_jwt_in_request()
    user_id = get_jwt_identity()
    return f"company_dashboard_{user_id}"

def student_dashboard_cache_key():
    verify_jwt_in_request()
    user_id = get_jwt_identity()
    return f"student_dashboard_{user_id}"