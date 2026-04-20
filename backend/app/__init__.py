from dotenv import load_dotenv
from flask import Flask
from app.models import db
from app.models.categoria import Categoria  
from app.models.movimiento_stock import MovimientoStock  
from app.models.producto import Producto 
from app.models.proveedor import Proveedor  
from app.models.rol import Rol 
from app.models.user import User  
from app.config import config
from app.routes.categoria_routes import categorias
from app.routes.movimiento_stock_routes import movimientos
from app.routes.producto_routes import productos
from app.routes.proveedor_routes import proveedores
from app.routes.auth_routes import auth_bp
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager, jwt_required

load_dotenv(override = True)
import os
migrate = Migrate()
jwt = JWTManager()

def create_app():
    app = Flask(__name__)
    env = os.getenv('FLASK_ENV', 'development')
    app.config.from_object(config[env])
    app.register_blueprint(auth_bp)
    app.register_blueprint(categorias)
    app.register_blueprint(proveedores)
    app.register_blueprint(productos)
    app.register_blueprint(movimientos)
    
    @app.route('/')
    @app.route('/<nombre>')    
    @jwt_required()
    def home(nombre = None):
        if (nombre == None):
            return f' <h1>Hola  desde programacion web dinamica 2026<h1>'
        return f'Hola {nombre} te saludamos desde programacion web dinamica 2026'

    @app.route('/saludo')
    @jwt_required()
    def saludo():
        return f'Hola desde programacion web dinamica 2026 saludo'
    db.init_app(app)
    migrate.init_app(app=app, db=db)
    jwt.init_app(app)
    return app
    
