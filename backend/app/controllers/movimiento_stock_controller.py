from typing import Any

from flask import Response, jsonify
from flask_jwt_extended import get_jwt_identity

from app.models import db
from app.models.movimiento_stock import MovimientoStock
from app.models.producto import Producto


class MovimientoStockController:
    @staticmethod
    def get_all() -> tuple[Response, int]:
        movimientos = db.session.execute(
            db.select(MovimientoStock).order_by(db.desc(MovimientoStock.id))
        ).scalars().all()
        return jsonify([movimiento.to_dict() for movimiento in movimientos]), 200

    @staticmethod
    def get_mis_movimientos() -> tuple[Response, int]:
        identity = get_jwt_identity()
        if identity is None:
            return jsonify({"message": "Usuario no autenticado"}), 401

        user_id = int(identity)
        movimientos = db.session.execute(
            db.select(MovimientoStock)
            .filter_by(user_id=user_id)
            .order_by(db.desc(MovimientoStock.id))
        ).scalars().all()
        return jsonify([movimiento.to_dict() for movimiento in movimientos]), 200

    @staticmethod
    def create(request: dict[str, Any] | None) -> tuple[Response, int]:
        request = request or {}
        tipo = request.get("tipo")
        cantidad_raw: Any = request.get("cantidad")
        producto_id = request.get("producto_id")
        motivo = request.get("motivo")

        if tipo not in ("entrada", "salida"):
            return jsonify({"message": "El tipo debe ser entrada o salida"}), 422

        try:
            cantidad_int = int(cantidad_raw)
        except (TypeError, ValueError):
            return jsonify({"message": "La cantidad debe ser un numero entero"}), 422

        if cantidad_int <= 0:
            return jsonify({"message": "La cantidad debe ser mayor a 0"}), 422

        if not isinstance(producto_id, int):
            return jsonify({"message": "El producto es requerido"}), 422

        producto = db.session.get(Producto, producto_id)
        if producto is None:
            return jsonify({"message": "Producto no encontrado"}), 404

        if tipo == "salida" and producto.stock_actual < cantidad_int:
            return (
                jsonify({"error": "Stock insuficiente para registrar la salida"}),
                409,
            )

        if tipo == "entrada":
            producto.stock_actual += cantidad_int
        else:
            producto.stock_actual -= cantidad_int

        identity = get_jwt_identity()
        if identity is None:
            return jsonify({"message": "Usuario no autenticado"}), 401

        movimiento = MovimientoStock(
            tipo=tipo,
            cantidad=cantidad_int,
            producto_id=producto_id,
            user_id=int(identity),
            motivo=movimiento_motivo(motivo),
        )
        db.session.add(movimiento)
        db.session.commit()
        return jsonify(movimiento.to_dict()), 201


def movimiento_motivo(value):
    if isinstance(value, str) and value.strip():
        return value.strip()
    return None
