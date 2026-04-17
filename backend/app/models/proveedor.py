from app.models import db

class Proveedor(db.Model):
    __tablename__="proveedores"
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False, unique=True)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())
    contacto = db.Column(db.String(255), nullable=True)
    telefono = db.Column(db.String(20), nullable=True)
    email = db.Column(db.String(255), nullable=True)

