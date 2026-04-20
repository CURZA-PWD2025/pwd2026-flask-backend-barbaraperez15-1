from app.models import db
from app.models.base_model import BaseModel


class Producto(BaseModel):
    __tablename__ = "productos"

    nombre = db.Column(db.String(150), nullable=False)
    descripcion = db.Column(db.Text, nullable=True)
    precio_costo = db.Column(db.Numeric(10, 2), nullable=False)
    precio_venta = db.Column(db.Numeric(10, 2), nullable=False)
    stock_actual = db.Column(db.Integer, default=0, nullable=False)
    stock_minimo = db.Column(db.Integer, default=0, nullable=False)
    categoria_id = db.Column(db.Integer, db.ForeignKey("categorias.id"), nullable=False)
    proveedor_id = db.Column(db.Integer, db.ForeignKey("proveedores.id"), nullable=True)

    categoria = db.relationship("Categoria", overlaps="productos")
    proveedor = db.relationship("Proveedor", overlaps="productos")
    movimientos_stock = db.relationship("MovimientoStock", overlaps="producto")

    def __init__(
        self,
        nombre: str,
        precio_costo,
        precio_venta,
        categoria_id: int,
        descripcion: str | None = None,
        stock_actual: int = 0,
        stock_minimo: int = 0,
        proveedor_id: int | None = None,
    ) -> None:
        self.nombre = nombre
        self.descripcion = descripcion
        self.precio_costo = precio_costo
        self.precio_venta = precio_venta
        self.stock_actual = stock_actual
        self.stock_minimo = stock_minimo
        self.categoria_id = categoria_id
        self.proveedor_id = proveedor_id

    def to_dict(self):
        return {
            "id": self.id,
            "nombre": self.nombre,
            "descripcion": self.descripcion,
            "precio_costo": str(self.precio_costo),
            "precio_venta": str(self.precio_venta),
            "stock_actual": self.stock_actual,
            "stock_minimo": self.stock_minimo,
            "categoria": (
                {"id": self.categoria.id, "nombre": self.categoria.nombre}
                if self.categoria
                else None
            ),
            "proveedor": (
                {"id": self.proveedor.id, "nombre": self.proveedor.nombre}
                if self.proveedor
                else None
            ),
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }
