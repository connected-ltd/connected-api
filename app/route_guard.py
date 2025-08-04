from flask import jsonify, g
from flask_jwt_extended import verify_jwt_in_request
from flask_jwt_extended import get_jwt
from flask_jwt_extended import get_jwt_identity


from functools import wraps

from app.user.model import User


def auth_required(*roles_required):
    def requires_auth(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            verify_jwt_in_request()
            claims = get_jwt()
            # check role
            if roles_required:
                if not (claims['role'] in roles_required):
                    return jsonify({"message": "Unauthorized to perform action"}), 401
            g.user = User.get_by_id(get_jwt_identity())
            return f(*args, **kwargs)
        return decorated
    return requires_auth

def admin_required():
    def requires_admin(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            verify_jwt_in_request()
            claims = get_jwt()
            # Check if the user has admin or super_admin role
            if claims.get('role') not in ['admin', 'super_admin']:
                return jsonify({"message": "Admin privileges required"}), 403
            g.user = User.get_by_id(get_jwt_identity())
            return f(*args, **kwargs)
        return decorated
    return requires_admin