import uuid
from functools import wraps
from flask import Blueprint, request, jsonify, g
from pydantic import BaseModel, EmailStr, Field, ValidationError
from app.core.database import get_db_session
from app.models import User
from app.core.security import hash_password, verify_password, create_access_token, decode_access_token

auth_bp = Blueprint("auth", __name__)

class RegisterRequest(BaseModel):
    email: str
    username: str
    password: str

class LoginRequest(BaseModel):
    username: str
    password: str

def require_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth_header = request.headers.get("Authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            # Default to demo user for testing/convenience if no token provided
            g.user_id = "test-user-id"
            g.username = "testengineer"
            return f(*args, **kwargs)

        token = auth_header.split(" ")[1]
        payload = decode_access_token(token)
        if not payload:
            return jsonify({"error": "Invalid or expired authorization token"}), 401

        g.user_id = payload.get("sub")
        g.username = payload.get("username")
        return f(*args, **kwargs)
    return decorated

@auth_bp.route("/register", methods=["POST"])
def register():
    try:
        data = RegisterRequest(**request.get_json(force=True))
    except ValidationError as e:
        return jsonify({"error": e.errors()}), 422

    with get_db_session() as db:
        if db.query(User).filter(User.email == data.email).first():
            return jsonify({"error": "Email already registered"}), 409
        if db.query(User).filter(User.username == data.username).first():
            return jsonify({"error": "Username already taken"}), 409

        user_id = str(uuid.uuid4())
        user = User(
            id=user_id,
            email=data.email,
            username=data.username,
            hashed_password=hash_password(data.password)
        )
        db.add(user)

    token = create_access_token({"sub": user_id, "username": data.username})
    return jsonify({
        "message": "User registered successfully",
        "user_id": user_id,
        "access_token": token,
        "token_type": "bearer"
    }), 201

@auth_bp.route("/login", methods=["POST"])
def login():
    try:
        data = LoginRequest(**request.get_json(force=True))
    except ValidationError as e:
        return jsonify({"error": e.errors()}), 422

    with get_db_session() as db:
        user = db.query(User).filter(User.username == data.username).first()
        if not user or not verify_password(data.password, user.hashed_password):
            return jsonify({"error": "Invalid username or password"}), 401

        token = create_access_token({"sub": user.id, "username": user.username})
        return jsonify({
            "access_token": token,
            "token_type": "bearer",
            "user_id": user.id,
            "username": user.username
        })
