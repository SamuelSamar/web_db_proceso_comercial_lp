from sqlalchemy import create_engine, text
import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(DATABASE_URL)

sql = """
CREATE TABLE IF NOT EXISTS empresas (
    empresa_id SERIAL PRIMARY KEY,
    ruc VARCHAR(11) NOT NULL UNIQUE,
    razon_social VARCHAR(255) NOT NULL,
    departamento VARCHAR(100)
);

CREATE TABLE IF NOT EXISTS contactos (
    contacto_id SERIAL PRIMARY KEY,
    empresa_id INT NOT NULL,
    correo VARCHAR(150),
    celular VARCHAR(50),
    representante VARCHAR(255),
    FOREIGN KEY (empresa_id) REFERENCES empresas(empresa_id)
);

CREATE TABLE IF NOT EXISTS procesos (
    proceso_id SERIAL PRIMARY KEY,
    empresa_id INT NOT NULL,
    tipo_proceso VARCHAR(100),
    objeto_contratacion VARCHAR(255),
    departamento_consultado VARCHAR(100),
    fecha DATE NOT NULL,
    fecha_envio TIMESTAMP NOT NULL,
    fecha_carga TIMESTAMP DEFAULT NOW(),
    FOREIGN KEY (empresa_id) REFERENCES empresas(empresa_id)
);

CREATE TABLE IF NOT EXISTS cargas (
    carga_id SERIAL PRIMARY KEY,
    nombre_archivo VARCHAR(255),
    fecha_carga TIMESTAMP DEFAULT NOW(),
    registros_insertados INT
);

CREATE UNIQUE INDEX IF NOT EXISTS idx_proceso_unico
ON procesos (empresa_id, tipo_proceso, fecha, fecha_envio);
"""

with engine.connect() as conn:
    conn.execute(text(sql))
    conn.commit()

print("Tablas creadas correctamente")