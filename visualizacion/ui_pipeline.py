import streamlit as st
import io
import contextlib

import Main as main
from validacion.validaciones import ejecutar_validaciones


def ejecutar_pipeline(ruta_archivo: str, log) -> None:
    st.subheader("Ejecución del pipeline")

    consola = io.StringIO()

    with st.spinner("Procesando archivo..."):
        try:
            with contextlib.redirect_stdout(consola):
                df_final, log = main.main(ruta_archivo, log)

            st.session_state["cleaned_df"]      = df_final
            st.session_state["trace_df"]        = log.obtener()
            st.session_state["console_output"]  = consola.getvalue()
            st.session_state["generated_files"] = main.exportar_datos(df_final, log)

            # ── Validaciones ──────────────────────────────────────────────────
            df_original = st.session_state.get("original_df")

            if df_original is not None:
                rv = ejecutar_validaciones(df_original, df_final, log)
                st.session_state["validation_df"] = rv.resumen()
                st.session_state["validation_ok"]  = not rv.hay_fallos()
            else:
                st.session_state["validation_df"] = None
                st.session_state["validation_ok"]  = None

            st.success("Pipeline ejecutado correctamente")

        except Exception as error:
            st.session_state["console_output"] = consola.getvalue()
            st.error(f"Error durante la ejecución: {error}")