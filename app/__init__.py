from flask import Flask
from config import Config
from flask_cors import CORS
from dotenv import load_dotenv

def create_app():
    # Nuevo
    load_dotenv()
    # Crear instancia Flask
    app = Flask(__name__)
    # Cargar configuración
    app.config.from_object(Config)

    CORS(app)
    # Registrar rutas (Blueprints)
    from app.routes.upload_routes import upload_bp
    app.register_blueprint(upload_bp)

    return app