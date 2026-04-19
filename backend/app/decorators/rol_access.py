from functools import wraps

from flask import jsonify
from flask_jwt_extended import get_jwt, verify_jwt_in_request


def rol_access(roles_permitidos):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            verify_jwt_in_request()
            claims = get_jwt()
            if claims.get("rol") in roles_permitidos:
                return func(*args, **kwargs)
            return (
                jsonify(
                    {
                        "msg": f"Acceso denegado: se requiere rol {' o '.join(roles_permitidos)}"
                    }
                ),
                403,
            )

        return wrapper

    return decorator
