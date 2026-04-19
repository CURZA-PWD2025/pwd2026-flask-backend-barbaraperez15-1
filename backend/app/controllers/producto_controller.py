from decimal import Decimal, InvalidOperation
from typing import Any

from flask import Response, jsonify
from sqlalchemy.exc import IntegrityError

from app.models import db
from app.models.categoria import Categoria
from app.models.producto import Producto
from app.models.proveedor import Proveedor


class ProductoController:
    @staticmethod
    def get_all() -> tuple[Response, int]:
        productos = db.session.execute(
            db.select(Producto).order_by(Producto.nombre)
        ).scalars().all()
        return jsonify([producto.to_dict() for producto in productos]), 200

    @staticmethod
    def show(id: int) -> tuple[Response, int]:
        producto = db.session.get(Producto, id)
        if producto is None:
            return jsonify({"message": "Producto no encontrado"}), 404
        return jsonify(producto.to_dict()), 200

    @staticmethod
    def create(request: dict | None) -> tuple[Response, int]:
        parsed, error_response = ProductoController._parse_payload(request)
        if error_response is not None:
            return error_response

        assert parsed is not None
        producto = Producto(**parsed)
        db.session.add(producto)
        db.session.commit()
        return jsonify(producto.to_dict()), 201

    @staticmethod
    def update(request: dict | None, id: int) -> tuple[Response, int]:
        producto = db.session.get(Producto, id)
        if producto is None:
            return jsonify({"message": "Producto no encontrado"}), 404

        parsed, error_response = ProductoController._parse_payload(request)
        if error_response is not None:
            return error_response

        assert parsed is not None
        for key, value in parsed.items():
            setattr(producto, key, value)

        try:
            db.session.commit()
            return jsonify(producto.to_dict()), 200
        except IntegrityError:
            db.session.rollback()
            return jsonify({"message": "No se pudo actualizar el producto"}), 409

    @staticmethod
    def destroy(id: int) -> tuple[Response, int]:
        producto = db.session.get(Producto, id)
        if producto is None:
            return jsonify({"message": "Producto no encontrado"}), 404

        try:
            db.session.delete(producto)
            db.session.commit()
            return jsonify({"message": "Producto eliminado con exito"}), 200
        except IntegrityError:
            db.session.rollback()
            return (
                jsonify(
                    {
                        "message": "No se puede eliminar el producto porque tiene movimientos asociados"
                    }
                ),
                409,
            )

    @staticmethod
    def _parse_payload(
        request: dict[str, Any] | None,
    ) -> tuple[dict[str, Any] | None, tuple[Response, int] | None]:
        request = request or {}

        nombre = request.get("nombre")
        if not isinstance(nombre, str) or not nombre.strip():
            return None, (jsonify({"message": "El nombre es requerido"}), 422)

        categoria_id = request.get("categoria_id")
        if not isinstance(categoria_id, int):
            return None, (jsonify({"message": "La categoria es requerida"}), 422)

        categoria = db.session.get(Categoria, categoria_id)
        if categoria is None:
            return None, (jsonify({"message": "Categoria no encontrada"}), 404)

        proveedor_id = request.get("proveedor_id")
        if proveedor_id is not None and not isinstance(proveedor_id, int):
            return None, (jsonify({"message": "El proveedor es invalido"}), 422)

        if proveedor_id is not None:
            proveedor = db.session.get(Proveedor, proveedor_id)
            if proveedor is None:
                return None, (jsonify({"message": "Proveedor no encontrado"}), 404)

        precio_costo = ProductoController._parse_decimal(request.get("precio_costo"))
        if precio_costo is None:
            return None, (jsonify({"message": "El precio_costo es requerido"}), 422)

        precio_venta = ProductoController._parse_decimal(request.get("precio_venta"))
        if precio_venta is None:
            return None, (jsonify({"message": "El precio_venta es requerido"}), 422)

        stock_actual = ProductoController._parse_int(request.get("stock_actual", 0))
        stock_minimo = ProductoController._parse_int(request.get("stock_minimo", 0))
        if stock_actual is None or stock_actual < 0:
            return None, (jsonify({"message": "El stock_actual es invalido"}), 422)
        if stock_minimo is None or stock_minimo < 0:
            return None, (jsonify({"message": "El stock_minimo es invalido"}), 422)

        parsed = {
            "nombre": nombre.strip(),
            "descripcion": ProductoController._clean_optional_text(
                request.get("descripcion")
            ),
            "precio_costo": precio_costo,
            "precio_venta": precio_venta,
            "stock_actual": stock_actual,
            "stock_minimo": stock_minimo,
            "categoria_id": categoria_id,
            "proveedor_id": proveedor_id,
        }
        return parsed, None

    @staticmethod
    def _parse_decimal(value: Any):
        if value is None or value == "":
            return None
        try:
            return Decimal(str(value))
        except (InvalidOperation, TypeError, ValueError):
            return None

    @staticmethod
    def _parse_int(value: Any) -> int | None:
        try:
            return int(value)
        except (TypeError, ValueError):
            return None

    @staticmethod
    def _clean_optional_text(value: Any) -> str | None:
        if isinstance(value, str) and value.strip():
            return value.strip()
        return None
