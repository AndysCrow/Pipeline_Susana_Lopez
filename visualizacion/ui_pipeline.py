import streamlit as st
import io
import contextlib

import Main as main


def ejecutar_pipeline(ruta_archivo: str, log) -> None:
    st.subheader("Ejecución del pipeline")

    consola = io.StringIO()

    with st.spinner("Procesando archivo..."):
        try:
            with contextlib.redirect_stdout(consola):
                df_final, log = main.main(ruta_archivo, log)

            st.session_state["cleaned_df"] = df_final
            st.session_state["trace_df"] = log.obtener()
            st.session_state["console_output"] = consola.getvalue()
            # Ahora generated_files es un dict {nombre_archivo: bytes}
            st.session_state["generated_files"] = main.exportar_datos(df_final, log)

            st.success("Pipeline ejecutado correctamente")

        except Exception as error:
            st.session_state["console_output"] = consola.getvalue()
            st.error(f"Error durante la ejecución: {error}")