import streamlit as st
import os
import sys

dir_file = os.path.dirname(os.path.abspath(__file__))
root_file = os.path.dirname(dir_file)
sys.path.append(root_file)

from trazabilidad.dataframe import LogTrazabilidad
from ui_archivos import cargar_archivo
from ui_pipeline import ejecutar_pipeline
from ui_resultados import mostrar_resultados


st.set_page_config(
    page_title="Pipeline de limpieza",
    layout="wide"
)

st.title("Pipeline de limpieza de morbilidad")

ruta_archivo = cargar_archivo()

if ruta_archivo is not None:
    log = LogTrazabilidad()

    if st.button("Procesar archivo", type="primary"):
        ejecutar_pipeline(ruta_archivo, log)

mostrar_resultados()