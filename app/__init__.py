from flask import Flask
from config import Config

def create_app():
    # Crear instancia Flask
    app = Flask(__name__)
    # Cargar configuración
    app.config.from_object(Config)
    # Registrar rutas (Blueprints)
    from app.routes.upload_routes import upload_bp
    app.register_blueprint(upload_bp)

    return app