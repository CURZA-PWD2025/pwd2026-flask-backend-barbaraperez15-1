from flask import Response, jsonify
from sqlalchemy.exc import IntegrityError

from app.models import db
from app.models.categoria import Categoria


class CategoriaController:
    @staticmethod
    def get_all() -> tuple[Response, int]:
        categorias = db.session.execute(
            db.select(Categoria).order_by(Categoria.nombre)
        ).scalars().all()
        return jsonify([categoria.to_dict() for categoria in categorias]), 200

    @staticmethod
    def show(id: int) -> tuple[Response, int]:
        categoria = db.session.get(Categoria, id)
        if categoria is None:
            return jsonify({"message": "Categoria no encontrada"}), 404
        return jsonify(categoria.to_dict()), 200

    @staticmethod
    def create(request: dict | None) -> tuple[Response, int]:
        request = request or {}
        nombre = request.get("nombre")
        descripcion = request.get("descripcion")

        if not isinstance(nombre, str) or not nombre.strip():
            return jsonify({"message": "El nombre es requerido"}), 422

        try:
            categoria = Categoria(
                nombre=nombre.strip(),
                descripcion=descripcion.strip()
                if isinstance(descripcion, str) and descripcion.strip()
                else None,
            )
            db.session.add(categoria)
            db.session.commit()
            return jsonify(categoria.to_dict()), 201
        except IntegrityError:
            db.session.rollback()
            return jsonify({"message": "La categoria ya existe"}), 409

    @staticmethod
    def update(request: dict | None, id: int) -> tuple[Response, int]:
        categoria = db.session.get(Categoria, id)
        if categoria is None:
            return jsonify({"message": "Categoria no encontrada"}), 404

        request = request or {}
        nombre = request.get("nombre")
        descripcion = request.get("descripcion")

        if not isinstance(nombre, str) or not nombre.strip():
            return jsonify({"message": "El nombre es requerido"}), 422

        categoria.nombre = nombre.strip()
        categoria.descripcion = (
            descripcion.strip()
            if isinstance(descripcion, str) and descripcion.strip()
            else None
        )

        try:
            db.session.commit()
            return jsonify(categoria.to_dict()), 200
        except IntegrityError:
            db.session.rollback()
            return jsonify({"message": "La categoria ya existe"}), 409

    @staticmethod
    def destroy(id: int) -> tuple[Response, int]:
        categoria = db.session.get(Categoria, id)
        if categoria is None:
            return jsonify({"message": "Categoria no encontrada"}), 404

        if categoria.productos:
            return (
                jsonify(
                    {
                        "message": "No se puede eliminar la categoria porque tiene productos asociados"
                    }
                ),
                409,
            )

        db.session.delete(categoria)
        db.session.commit()
        return jsonify({"message": "Categoria eliminada con exito"}), 200
