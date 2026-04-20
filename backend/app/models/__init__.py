from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

from app.models.base_model import BaseModel  
from app.models.rol import Rol 
from app.models.user import User  
from app.models.categoria import Categoria 
from app.models.proveedor import Proveedor  
from app.models.producto import Producto  
from app.models.movimiento_stock import MovimientoStock
