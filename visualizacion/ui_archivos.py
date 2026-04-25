import streamlit as st
import pandas as pd
import os


def cargar_archivo() -> str | None:
    uploaded_file = st.file_uploader(
        "Sube el archivo de entrada",
        type=["xlsb"]
    )

    if uploaded_file is None:
        return None

    ruta = "data/database.xlsb"

    os.makedirs("data", exist_ok=True)

    with open(ruta, "wb") as f:
        f.write(uploaded_file.read())

    st.success("Archivo cargado correctamente")

    try:
        df_preview = pd.read_excel(ruta, engine="pyxlsb", nrows=5)

        st.subheader("Vista previa del archivo cargado")
        st.dataframe(
            df_preview,
            use_container_width=True,
            hide_index=True
        )

    except Exception as error:
        st.warning(f"No se pudo mostrar la vista previa: {error}")

    return ruta