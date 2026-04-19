from app.models import db
from app.models.base_model import BaseModel


class Rol(BaseModel):
    __tablename__ = "roles"

    nombre = db.Column(db.String(100), unique=True, nullable=False)
    activo = db.Column(db.String(1), default="S")
    users = db.relationship("User", overlaps="rol")

    def __init__(self, nombre) -> None:
        self.nombre = nombre

    def to_dict(self):
        return {
            "id": self.id,
            "nombre": self.nombre,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }
