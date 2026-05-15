import streamlit as st
import pandas as pd
import tempfile


def cargar_archivo() -> str | None:

    uploaded_file = st.file_uploader(
        "Sube el archivo de entrada",
        type=["xlsb"]
    )

    # Si se quitó el archivo, limpiar sesión
    if uploaded_file is None:
        for k in ["ruta_temp", "uploaded_filename", "original_df", "df_preview"]:
            st.session_state.pop(k, None)
        return None

    # Solo procesar si es un archivo nuevo
    if st.session_state.get("uploaded_filename") != uploaded_file.name:

        tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".xlsb", prefix="pipeline_")
        tmp.write(uploaded_file.read())
        tmp.flush()
        tmp.close()

        with st.spinner("Cargando archivo..."):
            try:
                # Una sola lectura completa
                df = pd.read_excel(tmp.name, engine="pyxlsb", dtype=str)
                df.columns = df.columns.str.strip().str.upper().str.replace(" ", "_")

                st.session_state["ruta_temp"]        = tmp.name
                st.session_state["uploaded_filename"] = uploaded_file.name
                st.session_state["original_df"]      = df
                st.session_state["df_preview"]       = df.head(5)

            except Exception as error:
                st.warning(f"No se pudo leer el archivo: {error}")
                return None

    # Mostrar resultado desde sesión (sin releer)
    st.success("Archivo cargado correctamente")
    st.subheader("Vista previa del archivo cargado")
    st.dataframe(st.session_state["df_preview"], use_container_width=True, hide_index=True)

    return st.session_state["ruta_temp"]