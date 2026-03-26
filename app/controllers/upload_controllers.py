import os
from flask import request, current_app
from app.services.etl_service import procesar_archivo

def manejar_upload():
    """
    Controlador que: recibe archivo, lo guarda, ejecuta ETL
    """

    file = request.files.get("file")
    if not file or file.filename == "":
        return {"error": "Archivo no válido"}
    
    # Guardar archivo en carpeta uploads
    upload_path = os.path.join(current_app.config["UPLOAD_FOLDER"], file.filename)
    file.save(upload_path)

    # Ejecutar ETL
    resultado = procesar_archivo(upload_path)

    return resultado