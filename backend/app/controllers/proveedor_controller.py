from flask import Response, jsonify
from sqlalchemy.exc import IntegrityError

from app.models import db
from app.models.proveedor import Proveedor


class ProveedorController:
    @staticmethod
    def get_all() -> tuple[Response, int]:
        proveedores = db.session.execute(
            db.select(Proveedor).order_by(Proveedor.nombre)
        ).scalars().all()
        return jsonify([proveedor.to_dict() for proveedor in proveedores]), 200

    @staticmethod
    def show(id: int) -> tuple[Response, int]:
        proveedor = db.session.get(Proveedor, id)
        if proveedor is None:
            return jsonify({"message": "Proveedor no encontrado"}), 404
        return jsonify(proveedor.to_dict()), 200

    @staticmethod
    def create(request: dict | None) -> tuple[Response, int]:
        request = request or {}
        nombre = request.get("nombre")

        if not isinstance(nombre, str) or not nombre.strip():
            return jsonify({"message": "El nombre es requerido"}), 422

        proveedor = Proveedor(
            nombre=nombre.strip(),
            contacto=ProveedorController._clean_optional_text(request.get("contacto")),
            telefono=ProveedorController._clean_optional_text(request.get("telefono")),
            email=ProveedorController._clean_optional_text(request.get("email")),
        )
        db.session.add(proveedor)
        db.session.commit()
        return jsonify(proveedor.to_dict()), 201

    @staticmethod
    def update(request: dict | None, id: int) -> tuple[Response, int]:
        proveedor = db.session.get(Proveedor, id)
        if proveedor is None:
            return jsonify({"message": "Proveedor no encontrado"}), 404

        request = request or {}
        nombre = request.get("nombre")
        if not isinstance(nombre, str) or not nombre.strip():
            return jsonify({"message": "El nombre es requerido"}), 422

        proveedor.nombre = nombre.strip()
        proveedor.contacto = ProveedorController._clean_optional_text(
            request.get("contacto")
        )
        proveedor.telefono = ProveedorController._clean_optional_text(
            request.get("telefono")
        )
        proveedor.email = ProveedorController._clean_optional_text(request.get("email"))
        db.session.commit()
        return jsonify(proveedor.to_dict()), 200

    @staticmethod
    def destroy(id: int) -> tuple[Response, int]:
        proveedor = db.session.get(Proveedor, id)
        if proveedor is None:
            return jsonify({"message": "Proveedor no encontrado"}), 404

        if proveedor.productos:
            return (
                jsonify(
                    {
                        "message": "No se puede eliminar el proveedor porque tiene productos asociados"
                    }
                ),
                409,
            )

        db.session.delete(proveedor)
        db.session.commit()
        return jsonify({"message": "Proveedor eliminado con exito"}), 200

    @staticmethod
    def _clean_optional_text(value):
        if isinstance(value, str) and value.strip():
            return value.strip()
        return None
