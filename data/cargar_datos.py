import pandas as pd
import os
import streamlit as st


def cargar_database(ruta_archivo: str) -> pd.DataFrame:

    # Si ya está cargado en sesión, reutilizarlo directamente
    if "original_df" in st.session_state:
        print("Usando DataFrame desde sesión (sin releer disco)")
        return st.session_state["original_df"].copy()

    if not os.path.exists(ruta_archivo):
        raise FileNotFoundError(f"El archivo {ruta_archivo} no existe")

    try:
        print(f"Leyendo archivo fuente: {ruta_archivo}")
        df = pd.read_excel(ruta_archivo, engine="pyxlsb", dtype=str)
    except Exception as e:
        raise RuntimeError(f"Error al leer el archivo Excel: {e}") from e

    df.columns = df.columns.str.strip().str.upper().str.replace(" ", "_")
    return df


def limpiar_cache():
    pass