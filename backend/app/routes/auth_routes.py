from flask import Blueprint, request
from flask_jwt_extended import jwt_required

from app.controllers.auth_controller import AuthController


auth_bp = Blueprint("auth", __name__, url_prefix="/auth")


@auth_bp.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    return AuthController.Register(data)


@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    return AuthController.login(data)


@auth_bp.route("/me", methods=["GET"])
@jwt_required()
def me():
    return AuthController.me()
