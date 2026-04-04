import os
# Configuración general del proyecto

class Config:
    UPLOAD_FOLDER = "uploads"
    # Leer desde variable de entorno
    # -----Nuevo----
    DATABASE_URL = os.getenv("DATABASE_URL")

    if DATABASE_URL:
        DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://")

    SQLALCHEMY_DATABASE_URI = DATABASE_URL
    # -----Fin Nuevo ----
    # Cadena de conexión a SQL Server
    #SQLALCHEMY_DATABASE_URI = (
    #    "mssql+pyodbc://@DESKTOP-2FH0I5C\\SQLEXPRESS01/db_proceso_empresarial?"
    #    "driver=ODBC+Driver+18+for+SQL+Server&trusted_connection=yes&TrustServerCertificate=yes&timeout=30"
    #)