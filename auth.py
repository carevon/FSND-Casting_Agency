from flask_jwt_extended import JWTManager, jwt_required, get_jwt
from functools import wraps

def setup_auth(app):
    jwt = JWTManager(app)

    @jwt.additional_claims_loader
    def add_claims_to_access_token(identity):
        return {
            'roles': identity['roles']
        }

    @jwt.user_identity_loader
    def user_identity_lookup(identity):
        return identity['username']

def requires_role(role):
    def decorator(fn):
        @wraps(fn)
        @jwt_required()
        def wrapper(*args, **kwargs):
            claims = get_jwt()
            if role not in claims['roles']:
                return {'message': 'Permission denied'}, 403
            return fn(*args, **kwargs)
        return wrapper
    return decorator
