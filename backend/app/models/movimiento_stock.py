from app.models import db
from app.models.base_model import BaseModel


class MovimientoStock(BaseModel):
    __tablename__ = "movimientos_stock"

    tipo = db.Column(db.String(10), nullable=False)
    cantidad = db.Column(db.Integer, nullable=False)
    motivo = db.Column(db.String(200), nullable=True)
    producto_id = db.Column(db.Integer, db.ForeignKey("productos.id"), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)

    producto = db.relationship("Producto", overlaps="movimientos_stock")
    user = db.relationship("User", overlaps="movimientos_stock")

    def __init__(
        self,
        tipo: str,
        cantidad: int,
        producto_id: int,
        user_id: int,
        motivo: str | None = None,
    ) -> None:
        self.tipo = tipo
        self.cantidad = cantidad
        self.producto_id = producto_id
        self.user_id = user_id
        self.motivo = motivo

    def to_dict(self):
        return {
            "id": self.id,
            "tipo": self.tipo,
            "cantidad": self.cantidad,
            "motivo": self.motivo,
            "producto": (
                {"id": self.producto.id, "nombre": self.producto.nombre}
                if self.producto
                else None
            ),
            "user": (
                {"id": self.user.id, "nombre": self.user.nombre}
                if self.user
                else None
            ),
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }
