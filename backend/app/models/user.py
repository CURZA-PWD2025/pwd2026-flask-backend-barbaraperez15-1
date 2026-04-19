from werkzeug.security import check_password_hash, generate_password_hash

from app.models import db
from app.models.base_model import BaseModel


class User(BaseModel):
    __tablename__ = "users"

    nombre = db.Column(db.String(100), unique=True, nullable=False)
    email = db.Column(db.String(200), unique=True, nullable=False)
    rol_id = db.Column(db.Integer, db.ForeignKey("roles.id"), nullable=False)
    password = db.Column(db.String(255), nullable=False)
    activo = db.Column(db.String(1), default="S", nullable=False)

    rol = db.relationship("Rol", overlaps="users")
    movimientos_stock = db.relationship("MovimientoStock", overlaps="user")

    def __init__(self, nombre: str, email: str, password: str, rol_id: int = 1) -> None:
        self.nombre = nombre
        self.email = email
        self.rol_id = rol_id
        self.password = password

    def __repr__(self):
        return f"usuario {self.nombre}, email {self.email} , fecha de creacion {self.created_at} "

    def to_dict(self):
        return {
            "id": self.id,
            "nombre": self.nombre,
            "email": self.email,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "rol": self.rol.to_dict() if self.rol else None,
        }

    def validate_password(self, password: str) -> bool:
        return check_password_hash(self.password, password)

    def generate_password(self, password: str):
        self.password = generate_password_hash(password)
