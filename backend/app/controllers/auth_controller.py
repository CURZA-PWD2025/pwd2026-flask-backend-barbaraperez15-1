from flask import Response, jsonify
from flask_jwt_extended import create_access_token, get_jwt_identity
from sqlalchemy.exc import IntegrityError

from app.models import db
from app.models.rol import Rol
from app.models.user import User


class AuthController:
    @staticmethod
    def Register(request: dict | None) -> tuple[Response, int]:
        request = request or {}
        nombre = request.get("nombre")
        email = request.get("email")
        password = request.get("password")

        if not isinstance(nombre, str) or not nombre.strip():
            return jsonify({"message": "El nombre es requerido"}), 422
        if not isinstance(email, str) or not email.strip():
            return jsonify({"message": "El email es requerido"}), 422
        if not isinstance(password, str) or not password.strip():
            return jsonify({"message": "La contrasena es requerida"}), 422

        try:
            rol_operador = db.session.execute(
                db.select(Rol).filter_by(nombre="operador")
            ).scalar_one_or_none()

            if rol_operador is None:
                rol_operador = Rol(nombre="operador")
                db.session.add(rol_operador)
                db.session.flush()

            user = User(
                nombre=nombre.strip(),
                email=email.strip(),
                rol_id=rol_operador.id,
                password=password,
            )
            user.generate_password(password)
            db.session.add(user)
            db.session.commit()

            return (
                jsonify(
                    {
                        "message": "usuario creado con exito",
                        "user": user.to_dict(),
                    }
                ),
                201,
            )
        except IntegrityError:
            db.session.rollback()
            return jsonify({"message": "Usuario ya registrado"}), 409

    @staticmethod
    def login(request: dict | None) -> tuple[Response, int]:
        request = request or {}
        nombre = request.get("nombre")
        password = request.get("password")

        if not isinstance(nombre, str) or not nombre.strip():
            return jsonify({"message": "El nombre es requerido"}), 422
        if not isinstance(password, str) or not password.strip():
            return jsonify({"message": "La contrasena es requerida"}), 422

        user = db.session.execute(
            db.select(User).filter_by(nombre=nombre.strip())
        ).scalar_one_or_none()

        if user and user.validate_password(password):
            access_token = create_access_token(
                identity=str(user.id),
                additional_claims={"rol": user.rol.nombre if user.rol else None},
            )
            return (
                jsonify(
                    {
                        "access_token": access_token,
                        "rol": user.rol.nombre if user.rol else None,
                        "nombre": user.nombre,
                    }
                ),
                200,
            )

        return jsonify({"message": "Credenciales invalidas"}), 401

    @staticmethod
    def me() -> tuple[Response, int]:
        user_id = get_jwt_identity()
        user = db.session.get(User, int(user_id))

        if user is None:
            return jsonify({"message": "Usuario no encontrado"}), 404

        return jsonify(user.to_dict()), 200
