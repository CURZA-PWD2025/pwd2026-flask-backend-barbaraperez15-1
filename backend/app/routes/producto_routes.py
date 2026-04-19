from flask import Blueprint, request
from flask_jwt_extended import jwt_required

from app.controllers.producto_controller import ProductoController
from app.decorators.rol_access import rol_access


productos = Blueprint("productos", __name__, url_prefix="/productos")


@productos.route("/", methods=["GET"])
@jwt_required()
def get_all():
    return ProductoController.get_all()


@productos.route("/<int:id>", methods=["GET"])
@jwt_required()
def show(id: int):
    return ProductoController.show(id)


@productos.route("/", methods=["POST"])
@jwt_required()
@rol_access(["admin"])
def create():
    return ProductoController.create(request.get_json())


@productos.route("/<int:id>", methods=["PUT"])
@jwt_required()
@rol_access(["admin"])
def update(id: int):
    return ProductoController.update(request.get_json(), id)


@productos.route("/<int:id>", methods=["DELETE"])
@jwt_required()
@rol_access(["admin"])
def destroy(id: int):
    return ProductoController.destroy(id)
