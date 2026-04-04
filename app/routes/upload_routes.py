from flask import Blueprint, render_template, jsonify
from app.controllers.upload_controllers import manejar_upload

upload_bp = Blueprint("upload", __name__)

@upload_bp.route("/upload", methods=["POST"])
def subir_archivo():
    # Llama al controlador
    resultado = manejar_upload()
    return jsonify(resultado)