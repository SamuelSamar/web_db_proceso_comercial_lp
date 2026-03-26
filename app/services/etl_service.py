import pandas as pd
from app.models.db import get_engine

def procesar_archivo(file_path):
    """
    - Limpiar datos
    - Insertar en SQL Server
    - Evitar duplicados
    """
    # --LIMPIEZA DE DATOS
    engine = get_engine()
    # Leer excel
    df = pd.read_excel(file_path, dtype=str)
    # Limpieza de datos
    df.columns = ["ruc", "razon_social", "departamento", "correo", "celular",
                  "representante", "tipo_proceso", "objeto_contratacion", "departamento_consultado", "fecha"]
    # Eliminar espacios
    df = df.apply(lambda col: col.str.strip() if col.dtype == "object" else col)
    # Convertir fecha
    df["fecha"] = pd.to_datetime(df["fecha"], errors="coerce").dt.date
    # Eliminar filas sin RUC
    df = df[df["ruc"].notna()]

    # --INSERTAR EN SQL SERVER
    # Empresas
    empresas = df[["ruc", "razon_social", "departamento"]].drop_duplicates()
    df_empresas_db = pd.read_sql("SELECT ruc FROM empresas", engine)
    empresas_nuevas = empresas[~empresas["ruc"].isin(df_empresas_db["ruc"])]

    if not empresas_nuevas.empty:
        empresas_nuevas.to_sql("empresas", engine, if_exists="append", index=False)
    
    # Obtener IDs
    df_empresas = pd.read_sql("SELECT empresa_id, ruc FROM empresas", engine)
    df = df.merge(df_empresas, on="ruc", how="left")

    #Contactos
    contactos = df[["empresa_id", "correo", "celular", "representante"]].drop_duplicates()
    df_contactos_db = pd.read_sql("SELECT empresa_id, correo, celular, representante FROM contactos", engine)
    contactos_nuevos = contactos.merge(df_contactos_db, on=["empresa_id", "correo", "celular", "representante"], how="left", indicator=True)
    contactos_nuevos = contactos_nuevos[contactos_nuevos["_merge"] == "left_only"].drop(columns=["_merge"])
    if not contactos_nuevos.empty:
        contactos_nuevos.to_sql("contactos", engine, if_exists="append", index=False)

    # Procesos
    procesos = df[["empresa_id", "tipo_proceso", "objeto_contratacion", "departamento_consultado", "fecha"]]
    df_db = pd.read_sql("SELECT empresa_id, tipo_proceso, fecha FROM procesos", engine)
    df_db["fecha"] = pd.to_datetime(df_db["fecha"]).dt.date
    procesos = procesos.merge(df_db, on=["empresa_id", "tipo_proceso", "fecha"], how="left", indicator=True)
    procesos_nuevos = procesos[procesos["_merge"] == "left_only"].drop(columns=["_merge"])

    if not procesos_nuevos.empty:
        procesos_nuevos.to_sql("procesos", engine, if_exists="append", index=False)
    
    # Cargas
    carga = pd.DataFrame([{
        "nombre_archivo": file_path,
        "registros_insertados": len(procesos_nuevos)
    }])
    carga.to_sql("cargas", engine, if_exists="append", index=False)

    return {
        "empresas_nuevas": len(empresas_nuevas),
        "procesos_insertados": len(procesos_nuevos)
    }