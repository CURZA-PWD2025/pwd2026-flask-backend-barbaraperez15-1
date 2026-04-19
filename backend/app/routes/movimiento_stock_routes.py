from flask import Blueprint, request
from flask_jwt_extended import jwt_required

from app.controllers.movimiento_stock_controller import MovimientoStockController
from app.decorators.rol_access import rol_access


movimientos = Blueprint("movimientos", __name__, url_prefix="/movimientos")


@movimientos.route("/", methods=["GET"])
@jwt_required()
@rol_access(["admin"])
def get_all():
    return MovimientoStockController.get_all()


@movimientos.route("/mis/", methods=["GET"])
@jwt_required()
def get_mis_movimientos():
    return MovimientoStockController.get_mis_movimientos()


@movimientos.route("/", methods=["POST"])
@jwt_required()
def create():
    return MovimientoStockController.create(request.get_json())
