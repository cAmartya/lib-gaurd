import os, jwt
from functools import wraps
from flask import request, redirect


# Verify JWT token
def verify_jwt(jwt_token):
    try:
        payload = jwt.decode(jwt_token, os.getenv("JWT_SECRET_KEY", "HS256"), algorithms=["HS256"])
        user_id = payload["user_id"]
        return user_id
    except jwt.ExpiredSignatureError:
        # expired
        return None
    except jwt.InvalidTokenError:
        # invalid
        return None


# Authentication
def auth_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        token = request.cookies.get("token")
        if not token:
            # Redirect to login page if token is not present
            return redirect("/login")
        user_id = verify_jwt(token)
        if not user_id:
            # Redirect to login page if token is invalid
            return redirect("/login")
        return func(*args, **kwargs)
    return wrapper
