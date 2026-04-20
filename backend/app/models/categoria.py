from app.models import db
from app.models.base_model import BaseModel


class Categoria(BaseModel):
    __tablename__ = "categorias"

    nombre = db.Column(db.String(100), nullable=False, unique=True)
    descripcion = db.Column(db.Text, nullable=True)

    productos = db.relationship("Producto", overlaps="categoria")

    def __init__(self, nombre: str, descripcion: str | None = None) -> None:
        self.nombre = nombre
        self.descripcion = descripcion

    def to_dict(self):
        return {
            "id": self.id,
            "nombre": self.nombre,
            "descripcion": self.descripcion,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }
