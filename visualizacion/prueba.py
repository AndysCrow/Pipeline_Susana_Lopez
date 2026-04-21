import streamlit as st
import pandas as pd
import os 
import sys

dir_file = os.path.dirname(os.path.abspath(__file__))
root_file = os.path.dirname(dir_file)
sys.path.append(root_file)
from trazabilidad.dataframe import LogTrazabilidad

import Main as main


st.title("Pipeline de limpieza")

uploaded_file = st.file_uploader("Sube el archivo de entrada", type=["xlsb"])
log = LogTrazabilidad()

if uploaded_file is not None:
    ruta = "data/database.xlsb"

    with open(ruta,"wb") as f:
        f.write(uploaded_file.read())

    st.success("Archivo cargado correctamente")

    if st.button("Procesar"):
        main.main(ruta, log)

if "cleaned_df" in st.session_state and "trace_df" in st.session_state:
    st.subheader("Vista previa")
    st.dataframe(st.session_state["cleaned_df"].head())

    cleaned_csv = st.session_state["cleaned_df"].to_csv(index=False).encode("utf-8")
    trace_csv = st.session_state["trace_df"].to_csv(index=False).encode("utf-8")

    st.download_button(
        "Descargar base limpia",
        data=cleaned_csv,
        file_name="cleaned_data.csv",
        mime="text/csv"
    )

    st.download_button(
        "Descargar trazabilidad",
        data=trace_csv,
        file_name="traceability.csv",
        mime="text/csv"
    )